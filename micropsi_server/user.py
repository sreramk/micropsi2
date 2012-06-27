"""
Very simple user management for the MicroPsi service

The user manager takes care of users, sessions and user roles.
If the user database is empty, we put a default user "admin" without a password and the role "Administrator" into it.
Users without a password set can login with an arbitrary password, so make sure that users do not set empty passwords
if this concerns you.

When new users are created, they are given a role and stored along with their hashed password. Because we do not store
the password itself, it cannot be retrieved if it is lost. Instead, set a new password.

Users, including the admin user, must be logged in to receive a valid session token. The session token is valid until
the user logs off, or until it expires. To prevent expiration, it may be refreshed during each user interaction.

To check the permissions of a given user, you may use get_permissions_for_session_token. In return, the user manager
will return the rights matrix of the associated user, if the user is logged in, or the rights of a guest it the session
token does not correspond to an open session.

At the moment, persistence is achieved with a simple file, into which user and session data is dumped in json format.

Example usage:

>>> um = UserManager()
>>> um.create_user("eliza", "qwerty", "World Creator")  # new user "eliza" with password "querty" as "World Creator"
>>> print um.list_users["eliza"]
{'is_active': False, 'role': 'World Creator'}
>>> elizas_token = um.start_session("eliza", "querty")  # log in eliza (give this token to her)
>>> print um.list_users["eliza"]
{'is_active': True, 'role': 'World Creator'}
>>> print um.get_permissions(elizas_token)
set(['manage worlds', 'manage agents'])
>>> um.set_user_role('eliza', 'Administrator')
>>> print um.get_permissions(elizas_token)
Set(['manage users', 'manage worlds', 'manage agents'])
>>> um.end_session(elizas_token)  # log off eliza
>>> print um.get_permissions(elizas_token)
{}
"""

__author__ = 'joscha'
__date__ = '11.05.12'

import json
import hashlib
import uuid
import os
import datetime
import threading
import time

ADMIN_USER = "admin"  # name of the admin user
USER_FILE_NAME = "user-data"  # resource files for all normal users
DEFAULT_ROLE = "Agent Creator"  # new users can create and edit agents, but not create worlds
IDLE_TIME_BEFORE_SESSION_EXPIRES = 360000  # after 100h idle time, expire the user session (but not the simulation)
TIME_INTERVAL_BETWEEN_EXPIRATION_CHECKS = 3600  # check every hour if we should log out users

USER_ROLES = {  # sets of strings; each represents a permission.
    "Administrator": {"manage users","manage worlds","manage agents", "manage server",
                      "create admin", "create restricted", "create full"},
    "Full": {"manage worlds","manage agents", "manage server" "create full", "create restricted"},
    "Restricted": {"manage agents", "create restricted"},
    "Guest": {"create restricted"}
}

class UserManager(object):
    """The user manager creates, deletes and authenticates users.

    It should be a singleton, because all user managers would use the same resources for maintaining persistence.

    Attributes:
        users: a dictionary of user_ids to user objects (containing session tokens, access role and hashed passwords)
        sessions: a dictionary of active sessions for faster reference
        user_file: the handle for the user data file
    """

    users = None
    sessions = {}

    def __init__(self, user_file_name = None):
        """initialize user management.

        If no user data are found, a new resource file is created.
        If you loose your admin password, you may delete the admin data from the resource file, so a new admin without
        password is created.

        Parameters:
            user_file (optional): a file like object to store user data permanently; will be updated after critical
                operations (new user, change password, shut down)
        """
        # set up persistence
        user_file_name = user_file_name or USER_FILE_NAME
        try:
            self.users = json.load(open(user_file_name))
        except ValueError, err:
            print "Could not read user data"
            self.users = {}

        self.user_file = open(user_file_name, "w+")

        # set up sessions
        for i in self.users:
            active_session = self.users[i]["session_token"]
            if active_session: self.sessions[active_session] = i

        # set up session cleanup
        def _session_expiration():
            while True:
                self.check_for_expired_user_sessions()
                time.sleep(TIME_INTERVAL_BETWEEN_EXPIRATION_CHECKS)

        session_expiration_daemon = threading.Thread(target=_session_expiration)
        session_expiration_daemon.daemon = True
        session_expiration_daemon.start()

    def __del__(self):
        """shut down user management"""
        self.save_users()

    def create_user(self, user_id, password="", role = DEFAULT_ROLE, uid = None):
        """create a new user.

        Returns False if the creation was not successful.

        Arguments:
            user_id: a non-empty string which must be unique, used for display and urls
            password: an arbitrary string
            role: a string corresponding to a user role (such as "Administrator", or "Agent Creator")
            uid: a string that acts as a unique, immutable handle (so we can store resources for this user)
        """
        if user_id and not user_id in self.users:
            self.users[user_id] = {
                "uid": uid or user_id,
                "hashed_password": hashlib.md5(password).hexdigest(),
                "role": role,
                "session_token": None,
                "session_expires": False
            }
            self.save_users()
            return True
        else: return False

    def save_users(self):
        """stores the user data to a file"""
        self.user_file.seek(0)
        json.dump(self.users, self.user_file, indent = 4)
        self.user_file.flush()

    def list_users(self):
        """returns a dictionary with all users currently known to the user manager for display purposes"""
        return { i: {
            "role": self.users[i]["role"],
            "is_active": True if self.users[i]["session_token"] else False }
                 for i in self.users }

    def set_user_id(self, user_id_old, user_id_new):
        """returns the new username if the user has been renamed successfully, the old username if the new one was
        already in use, and None if the old username did not exist"""
        if user_id_old in self.users:
            if not user_id_new in self.users:
                self.users[user_id_new] = self.users[user_id_old]
                del self.users[user_id_old]
                self.save_users()
                return user_id_new
            else:
                return user_id_old
        return None

    def set_user_role(self, user_id, role):
        """sets the role, and thereby the permissions of a user, returns False if user does not exist"""
        if user_id in self.users:
            self.users[user_id]["role"] = role
            self.save_users()
            return True
        return False

    def set_user_password(self, user_id, password):
        """sets the password of a user, returns False if user does not exist"""
        if user_id in self.users:
            self.users[user_id]["hashed_password"] = hashlib.md5(password).hexdigest()
            self.save_users()
            return True
        return False

    def delete_user(self, user_id):
        """deletes the specified user, returns True if successful"""
        if user_id in self.users:
            # if the user is still active, kill the session
            if self.users[user_id]["session_token"]: self.end_session(self.users[user_id]["session_token"])
            del self.users[user_id]
            self.save_users()
            return True
        return False

    def start_session(self, user_id, password="", keep_logged_in_forever=True):
        """authenticates the specified user, returns session token if successful, or None if not.

        Arguments:
            user_id: a string that must be the id of an existing user
            password (optional): checked against the stored password
            keep_logged_in_forever (optional): if True, the session will not expire unless manually logging off
        """
        if self.test_password(user_id, password):
            session_token = str(uuid.UUID(bytes = os.urandom(16)))
            self.users[user_id]["session_token"] = session_token
            self.sessions[session_token] = user_id
            if keep_logged_in_forever:
                self.users[user_id]["session_expires"] = False
                self.save_users()
            else:
                self.refresh_session(session_token)
            return session_token
        return None

    def test_password(self, user_id, password):
        """returns True if the user is known and the password matches, False otherwise"""
        if user_id in self.users:
            if self.users[user_id]["hashed_password"] == hashlib.md5(password).hexdigest():
                return True
        return False

    def end_session(self, session_token):
        """ends the session associated with the given token"""
        if session_token in self.sessions:
            user_id = self.sessions[session_token]
            del self.sessions[session_token]
            if user_id in self.users:
                self.users[user_id]["session_token"] = None

    def end_all_sessions(self):
        """useful during a reset of the runtime, because all open user sessions will persist during shutdown"""
        for session_token in self.sessions: self.end_session(session_token)

    def refresh_session(self, session_token):
        """resets the idle time until a currently active session expires to some point in the future"""
        if session_token in self.sessions:
            user_id = self.sessions[session_token]
            if self.users[user_id]["session_expires"]:
                self.users[user_id]["session_expires"] = datetime.datetime.now() + datetime.timedelta(
                    seconds=IDLE_TIME_BEFORE_SESSION_EXPIRES)

    def check_for_expired_user_sessions(self):
        """removes all user sessions that have been idle for too long"""

        change_flag = False
        for session_token in self.sessions:
            user_id = self.sessions[session_token]
            if self.users[user_id]["session_expires"]:
                if self.users[user_id]["session_expires"] < datetime.datetime.now():
                    self.end_session(session_token)
                    change_flag = True
        if change_flag:
            self.save_users()

    def get_permissions_for_session_token(self, session_token):
        """returns a set of permissions corresponding to the role of the user associated with the session;
        if no session with that token exists, the Guest role permissions are returned.

        Example usage:
            if "create agents" in usermanager.get_permissions(my_session): ...
        """

        if session_token in self.sessions:
            user_id = self.sessions[session_token]
            if user_id in self.users:
                role = self.users[user_id]["role"]
                if role in USER_ROLES:
                    return USER_ROLES[role]

        return USER_ROLES["Guest"]

    def get_user_id_for_session_token(self, session_token):
        """returns the id of the user associated with the session token, or 'Guest', if the token is invalid"""

        if session_token in self.sessions:
            return self.sessions[session_token]
        else:
            return "Guest"

def check_for_url_proof_id(id, existing_ids = None, min_id_length = 1, max_id_length = 21):
    """Returns (True, id) if id is permissible, and (False, error message) otherwise. Since
    we strip the id, you should use the returned one, not the original one"""

    id = id.strip()

    # maybe this is too restrictive, but I want to use the id directly in urls
    for c in id:
        if not c.lower() in "0123456789abcdefghijklmnopqrstuvwxyz@._-":
            return False, "The character '%s' is not allowed" %c

    if existing_ids and id.lower() in existing_ids: return False, "ID already exists"
    if len(id) < min_id_length:
        return False, "Must at least have %s characters" % min_id_length
    if len(id) > max_id_length:
        return False, "Must have less than %s characters" % max_id_length

    return True, id