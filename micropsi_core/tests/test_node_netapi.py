#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Tests for netapi, i.e. the interface native modules will be developed against
"""

import pytest
from micropsi_core import runtime as micropsi


def prepare(fixed_nodenet):
    nodenet = micropsi.get_nodenet(fixed_nodenet)
    netapi = nodenet.netapi
    source = netapi.create_node("Register", None, "Source")
    netapi.link(source, "gen", source, "gen")
    source.activation = 1
    nodenet.step()
    return nodenet, netapi, source


def test_node_netapi_create_register_node(fixed_nodenet):
    # test register node creation
    net, netapi, source = prepare(fixed_nodenet)
    node = netapi.create_node("Register", None, "TestName")

    # basic logic tests
    assert node is not None
    root_ns = netapi.get_nodespace(None)
    assert node.parent_nodespace == root_ns.uid
    assert node.type == "Register"
    assert node.uid is not None
    assert len(node.get_gate('gen').get_links()) == 0
    assert len(node.get_gate('gen').activations) == 1

    # frontend/persistency-oriented data dictionary test
    data = node.get_data()
    assert data['uid'] == node.uid
    assert data['name'] == node.name
    assert data['type'] == node.type

    node = netapi.create_node("Register", None)
    # TODO: teh weirdness, server-internally, we return uids as names, clients don't see this, confusion ensues
    # assert data['name'] == node.name


def test_node_netapi_create_pipe_node(fixed_nodenet):
    # test concept node generation
    net, netapi, source = prepare(fixed_nodenet)
    node = netapi.create_node("Pipe", None, "TestName")

    # basic logic tests
    assert node is not None
    assert node.parent_nodespace == netapi.get_nodespace(None).uid
    assert node.type == "Pipe"
    assert node.uid is not None
    assert len(node.get_gate('gen').get_links()) == 0
    assert len(node.get_gate('gen').activations) == 1
    assert len(node.get_gate('sub').get_links()) == 0
    assert len(node.get_gate('sub').activations) == 1
    assert len(node.get_gate('sur').get_links()) == 0
    assert len(node.get_gate('sur').activations) == 1
    assert len(node.get_gate('por').get_links()) == 0
    assert len(node.get_gate('por').activations) == 1
    assert len(node.get_gate('ret').get_links()) == 0
    assert len(node.get_gate('ret').activations) == 1
    assert len(node.get_gate('cat').get_links()) == 0
    assert len(node.get_gate('cat').activations) == 1
    assert len(node.get_gate('exp').get_links()) == 0
    assert len(node.get_gate('exp').activations) == 1

    # frontend/persistency-oriented data dictionary test
    data = node.get_data()
    assert data['uid'] == node.uid
    for key in node.get_gate_types():
        assert key not in data['gate_parameters']
        for parameter, value in node.nodetype.gate_defaults[key].items():
            assert node.get_gate(key).get_parameter(parameter) == value
    assert data['name'] == node.name
    assert data['type'] == node.type

    node = netapi.create_node("Pipe", None)
    # TODO: teh weirdness, server-internally, we return uids as names, clients don't see this, confusion ensues
    # assert data['name'] == node.name


@pytest.mark.engine("dict_engine")
def test_node_netapi_create_concept_node(fixed_nodenet):
    # test concept node generation
    net, netapi, source = prepare(fixed_nodenet)
    node = netapi.create_node("Concept", None, "TestName")

    # basic logic tests
    assert node is not None
    assert node.parent_nodespace == netapi.get_nodespace(None).uid
    assert node.type == "Concept"
    assert node.uid is not None
    assert len(node.get_gate('gen').get_links()) == 0
    assert len(node.get_gate('gen').activations) == 1
    assert len(node.get_gate('sub').get_links()) == 0
    assert len(node.get_gate('sub').activations) == 1
    assert len(node.get_gate('sur').get_links()) == 0
    assert len(node.get_gate('sur').activations) == 1
    assert len(node.get_gate('por').get_links()) == 0
    assert len(node.get_gate('por').activations) == 1
    assert len(node.get_gate('ret').get_links()) == 0
    assert len(node.get_gate('ret').activations) == 1
    assert len(node.get_gate('cat').get_links()) == 0
    assert len(node.get_gate('cat').activations) == 1
    assert len(node.get_gate('exp').get_links()) == 0
    assert len(node.get_gate('exp').activations) == 1
    assert len(node.get_gate('sym').get_links()) == 0
    assert len(node.get_gate('sym').activations) == 1
    assert len(node.get_gate('ref').get_links()) == 0
    assert len(node.get_gate('ref').activations) == 1

    # frontend/persistency-oriented data dictionary test
    data = node.get_data()
    assert data['uid'] == node.uid
    assert data['name'] == node.name
    assert data['type'] == node.type

    node = netapi.create_node("Pipe", None)
    # TODO: teh weirdness, server-internally, we return uids as names, clients don't see this, confusion ensues
    # assert data['name'] == node.name


def test_node_netapi_create_node_in_nodespace(fixed_nodenet):
    # test register node in nodespace creation
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node = netapi.create_node("Register", nodespace.uid, "TestName")

    assert node.parent_nodespace == nodespace.uid
    assert node.get_data()['parent_nodespace'] == nodespace.uid


def test_node_netapi_get_nodespace_one(fixed_nodenet):
    # test single nodespace querying
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "TestName")

    queried_nodespace = netapi.get_nodespace(nodespace.uid)
    assert queried_nodespace.uid == nodespace.uid
    assert queried_nodespace.name == nodespace.name


def test_node_netapi_get_nodespace_multi(fixed_nodenet):
    # test nodespace listing
    net, netapi, source = prepare(fixed_nodenet)
    nodespace1 = netapi.create_nodespace(None, "TestName1")
    nodespace2 = netapi.create_nodespace(None, "TestName2")
    nodespace3 = netapi.create_nodespace(nodespace2.uid, "TestName3")
    root_ns = netapi.get_nodespace(None)
    queried_nodespaces = netapi.get_nodespaces(root_ns.uid)
    assert len(queried_nodespaces) == 2
    assert nodespace1.uid in [x.uid for x in queried_nodespaces]
    assert nodespace2.uid in [x.uid for x in queried_nodespaces]
    assert nodespace3.uid not in [x.uid for x in queried_nodespaces]


def test_node_netapi_get_node(fixed_nodenet):
    # test register node creation
    net, netapi, source = prepare(fixed_nodenet)
    node = netapi.create_node("Register", None, "TestName")

    queried_node = netapi.get_node(node.uid)
    assert queried_node.uid == node.uid
    assert queried_node.name == node.name
    assert queried_node.get_data() == node.get_data()
    assert queried_node.type == node.type


def test_node_netapi_get_nodes(fixed_nodenet):
    # test get_nodes plain
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")

    nodes = netapi.get_nodes(netapi.get_nodespace(None).uid)
    assert node1.uid in [n.uid for n in nodes]
    assert node2.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_by_name(fixed_nodenet):
    # test get_nodes by name
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")

    nodes = netapi.get_nodes(netapi.get_nodespace(None).uid, node_name_prefix="TestName")
    assert len(nodes) == 2
    assert node1.uid in [n.uid for n in nodes]
    assert node2.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_by_nodespace(fixed_nodenet):
    # test get_nodes by name and nodespace
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Register", nodespace.uid, "TestName1")
    node2 = netapi.create_node("Register", nodespace.uid, "TestName2")

    nodes = netapi.get_nodes(nodespace.uid)
    assert len(nodes) == 2
    assert node1.uid in [n.uid for n in nodes]
    assert node2.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_by_nodetype(fixed_nodenet):
    # test get_nodes by name and nodespace
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Pipe", nodespace.uid, "TestName1")
    node2 = netapi.create_node("Register", nodespace.uid, "TestName2")

    nodes = netapi.get_nodes(nodetype="Register")
    assert len(nodes) == 2
    uids = [n.uid for n in nodes]
    assert node1.uid not in uids
    assert node2.uid in uids
    assert source.uid in uids


def test_node_netapi_get_nodes_by_name_and_nodespace(fixed_nodenet):
    # test get_nodes by name and nodespace
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", nodespace.uid, "TestName2")

    nodes = netapi.get_nodes(nodespace.uid, "TestName")
    assert len(nodes) == 1
    assert node2.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_in_gate_field(fixed_nodenet):
    # test get_nodes_in_gate_field
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Pipe", None, "TestName1")
    node2 = netapi.create_node("Pipe", None, "TestName2")
    node3 = netapi.create_node("Pipe", None, "TestName3")
    node4 = netapi.create_node("Pipe", None, "TestName4")
    netapi.link_with_reciprocal(node1, node2, "subsur")
    netapi.link_with_reciprocal(node1, node3, "subsur")
    netapi.link_with_reciprocal(node1, node4, "subsur")
    netapi.link_with_reciprocal(node2, node3, "porret")

    nodes = netapi.get_nodes_in_gate_field(node1, "sub")
    assert len(nodes) == 3
    assert node2.uid in [n.uid for n in nodes]
    assert node3.uid in [n.uid for n in nodes]
    assert node4.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_in_gate_field_all_links(fixed_nodenet):
    # test get_nodes_in_gate_field without specifying a gate parameter
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Pipe", None, "TestName1")
    node2 = netapi.create_node("Pipe", None, "TestName2")
    node3 = netapi.create_node("Pipe", None, "TestName3")
    node4 = netapi.create_node("Pipe", None, "TestName4")
    netapi.link_with_reciprocal(node1, node2, "subsur")
    netapi.link_with_reciprocal(node1, node3, "subsur")
    netapi.link_with_reciprocal(node1, node4, "subsur")
    netapi.link_with_reciprocal(node2, node3, "porret")

    nodes = netapi.get_nodes_in_gate_field(node2)
    assert len(nodes) == 2
    assert node1.uid in [n.uid for n in nodes]
    assert node3.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_in_gate_field_with_limitations(fixed_nodenet):
    # test get_nodes_in_gate_field with limitations: no por links
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Pipe", None, "TestName1")
    node2 = netapi.create_node("Pipe", None, "TestName2")
    node3 = netapi.create_node("Pipe", None, "TestName3")
    node4 = netapi.create_node("Pipe", None, "TestName4")
    netapi.link_with_reciprocal(node1, node2, "subsur")
    netapi.link_with_reciprocal(node1, node3, "subsur")
    netapi.link_with_reciprocal(node1, node4, "subsur")
    netapi.link_with_reciprocal(node2, node3, "porret")

    nodes = netapi.get_nodes_in_gate_field(node1, "sub", ["por"])
    assert len(nodes) == 2
    assert node3.uid in [n.uid for n in nodes]
    assert node4.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_in_gate_field_with_limitations_and_nodespace(fixed_nodenet):
    # test get_nodes_in_gate_field with limitations: no por links
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Pipe", None, "TestName1")
    node2 = netapi.create_node("Pipe", None, "TestName2")
    node3 = netapi.create_node("Pipe", None, "TestName3")
    node4 = netapi.create_node("Pipe", nodespace.uid, "TestName4")
    netapi.link_with_reciprocal(node1, node2, "subsur")
    netapi.link_with_reciprocal(node1, node3, "subsur")
    netapi.link_with_reciprocal(node1, node4, "subsur")
    netapi.link_with_reciprocal(node2, node3, "porret")
    nodes = netapi.get_nodes_in_gate_field(node1, "sub", ["por"], netapi.get_nodespace(None).uid)
    assert len(nodes) == 1
    assert node3.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_in_slot_field(fixed_nodenet):
    # test get_nodes_in_slot_field
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    node3 = netapi.create_node("Register", None, "TestName3")
    node4 = netapi.create_node("Register", None, "TestName4")
    netapi.link(node2, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node4, "gen", node1, "gen")

    nodes = netapi.get_nodes_in_slot_field(node1, "gen")
    assert len(nodes) == 3
    assert node2.uid in [n.uid for n in nodes]
    assert node3.uid in [n.uid for n in nodes]
    assert node4.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_in_slot_field_all_links(fixed_nodenet):
    # test get_nodes_in_slot_field without a gate parameter
    net, netapi, source = prepare(fixed_nodenet)
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Pipe", None, "TestName1")
    node2 = netapi.create_node("Pipe", None, "TestName2")
    node3 = netapi.create_node("Pipe", None, "TestName3")
    node4 = netapi.create_node("Pipe", None, "TestName4")
    netapi.link_with_reciprocal(node1, node2, "subsur")
    netapi.link_with_reciprocal(node1, node3, "subsur")
    netapi.link_with_reciprocal(node1, node4, "subsur")
    netapi.link_with_reciprocal(node2, node3, "porret")

    nodes = netapi.get_nodes_in_slot_field(node1)
    assert len(nodes) == 3
    assert node2.uid in [n.uid for n in nodes]
    assert node3.uid in [n.uid for n in nodes]
    assert node4.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_with_nodespace_limitation(fixed_nodenet):
    # test get_nodes_feed with nodespace limitation
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    node3 = netapi.create_node("Register", None, "TestName3")
    node4 = netapi.create_node("Register", nodespace.uid, "TestName4")
    netapi.link(node2, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node4, "gen", node1, "gen")

    nodes = netapi.get_nodes_in_slot_field(node1, "gen", None, netapi.get_nodespace(None).uid)
    assert len(nodes) == 2
    assert node2.uid in [n.uid for n in nodes]
    assert node3.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_in_slot_field_with_limitations_and_nodespace(fixed_nodenet):
    # test get_nodes_in_gate_field with limitations: no por links
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Pipe", None, "TestName1")
    node2 = netapi.create_node("Pipe", None, "TestName2")
    node3 = netapi.create_node("Pipe", None, "TestName3")
    node4 = netapi.create_node("Pipe", nodespace.uid, "TestName4")
    netapi.link_with_reciprocal(node1, node2, "subsur")
    netapi.link_with_reciprocal(node1, node3, "subsur")
    netapi.link_with_reciprocal(node1, node4, "subsur")
    netapi.link_with_reciprocal(node2, node3, "porret")
    nodes = netapi.get_nodes_in_slot_field(node1, "sur", ["por"], netapi.get_nodespace(None).uid)
    assert len(nodes) == 1
    assert node3.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_active(fixed_nodenet):
    # test get_nodes_active
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    node3 = netapi.create_node("Register", None, "TestName3")
    node4 = netapi.create_node("Register", nodespace.uid, "TestName4")
    netapi.link(node2, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node4, "gen", node1, "gen")
    netapi.link(source, "gen", node2, "gen", 0.5)
    netapi.link(source, "gen", node4, "gen", 0.5)

    net.step()
    net.step()

    nodes = netapi.get_nodes_active(netapi.get_nodespace(None).uid, "Register", 0.7, "gen")
    assert len(nodes) == 2
    assert node1.uid in [n.uid for n in nodes]
    assert source.uid in [n.uid for n in nodes]

    nodes = netapi.get_nodes_active(netapi.get_nodespace(None).uid, "Register")
    assert len(nodes) == 2
    assert node1.uid in [n.uid for n in nodes]
    assert source.uid in [n.uid for n in nodes]


def test_node_netapi_get_nodes_active_with_nodespace_limitation(fixed_nodenet):
    # test get_nodes_active with nodespace filtering
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    node3 = netapi.create_node("Register", None, "TestName3")
    node4 = netapi.create_node("Register", nodespace.uid, "TestName4")
    netapi.link(node2, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node4, "gen", node1, "gen")
    netapi.link(source, "gen", node2, "gen", 0.5)
    netapi.link(source, "gen", node4, "gen", 0.5)

    net.step()
    net.step()

    nodes = netapi.get_nodes_active(nodespace.uid, "Register", 0.4)
    assert len(nodes) == 1
    assert node4.uid in [n.uid for n in nodes]


def test_node_netapi_delete_node(fixed_nodenet):
    # test simple delete node case
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    node3 = netapi.create_node("Register", None, "TestName3")
    netapi.link(node2, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")

    olduid = node1.uid
    netapi.delete_node(node1)
    with pytest.raises(KeyError):
        netapi.get_node(olduid)
    assert len(node2.get_gate("gen").get_links()) == 0


def test_node_netapi_delete_nodespace(fixed_nodenet):
    # test delete node case deleting a nodespace
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, "NestedNodespace")
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    node3 = netapi.create_node("Register", None, "TestName3")
    node4 = netapi.create_node("Register", nodespace.uid, "TestName4")
    netapi.link(node2, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node3, "gen", node1, "gen")
    netapi.link(node4, "gen", node1, "gen")

    node4uid = node4.uid
    netapi.delete_nodespace(nodespace)
    with pytest.raises(KeyError):
        netapi.get_node(node4uid)


def test_node_netapi_link(fixed_nodenet):
    # test linking nodes
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    netapi.link(node2, "gen", node1, "gen")

    assert len(node2.get_gate("gen").get_links()) == 1
    for link in node2.get_gate("gen").get_links():
        # basic internal logic
        assert link.source_node.uid == node2.uid
        assert link.target_node.uid == node1.uid
        assert link.weight == 1

        found = False
        for otherside_link in node1.get_slot("gen").get_links():
            if otherside_link.signature == link.signature:
                found = True
        assert found

        # frontend/persistency-facing
        assert link.get_data()['weight'] == link.weight
        assert link.get_data()['target_node_uid'] == node1.uid
        assert link.get_data()['target_slot_name'] == 'gen'
        # frontend/persistency-facing
        assert link.get_data(complete=True)['source_node_uid'] == node2.uid
        assert link.get_data(complete=True)['source_gate_name'] == 'gen'


def test_node_netapi_link_change_weight(fixed_nodenet):
    # test linking nodes, the changing weights
    net, netapi, source = prepare(fixed_nodenet)
    node1 = netapi.create_node("Register", None, "TestName1")
    node2 = netapi.create_node("Register", None, "TestName2")
    netapi.link(node2, "gen", node1, "gen")

    net.step()

    netapi.link(node2, "gen", node1, "gen", 0.8)

    assert len(node2.get_gate("gen").get_links()) == 1
    for link in node2.get_gate("gen").get_links():
        # basic internal logic
        assert link.source_node.uid == node2.uid
        assert link.target_node.uid == node1.uid
        assert round(link.weight, 5) == 0.8

        found = False
        for otherside_link in node1.get_slot("gen").get_links():
            if otherside_link.signature == link.signature:
                found = True
        assert found

        # frontend/persistency-facing
        assert link.get_data()['weight'] == link.weight
        assert link.get_data()['target_node_uid'] == node1.uid
        assert link.get_data()['target_slot_name'] == 'gen'


def test_node_netapi_link_with_reciprocal(fixed_nodenet):
    # test linking pipe and concept nodes with reciprocal links
    net, netapi, source = prepare(fixed_nodenet)
    n_head = netapi.create_node("Pipe", None, "Head")
    n_a = netapi.create_node("Pipe", None, "A")
    n_b = netapi.create_node("Pipe", None, "B")
    n_c = netapi.create_node("Pipe", None, "C")
    netapi.link_with_reciprocal(n_head, n_a, "subsur")
    netapi.link_with_reciprocal(n_head, n_b, "subsur")
    netapi.link_with_reciprocal(n_head, n_c, "subsur")
    netapi.link_with_reciprocal(n_a, n_b, "porret", 0.5)
    netapi.link_with_reciprocal(n_b, n_c, "porret", 0.5)

    assert len(n_head.get_gate("sub").get_links()) == 3
    assert len(n_head.get_slot("sur").get_links()) == 3
    assert len(n_a.get_gate("sur").get_links()) == 1
    assert len(n_a.get_slot("sub").get_links()) == 1
    assert len(n_b.get_gate("sur").get_links()) == 1
    assert len(n_b.get_slot("sub").get_links()) == 1
    assert len(n_c.get_gate("sur").get_links()) == 1
    assert len(n_c.get_slot("sub").get_links()) == 1
    assert len(n_a.get_gate("por").get_links()) == 1
    assert len(n_a.get_slot("ret").get_links()) == 1
    assert len(n_a.get_slot("por").get_links()) == 0
    assert len(n_b.get_gate("por").get_links()) == 1
    assert len(n_b.get_slot("ret").get_links()) == 1
    assert len(n_b.get_gate("ret").get_links()) == 1
    assert len(n_b.get_slot("por").get_links()) == 1
    assert len(n_c.get_gate("por").get_links()) == 0
    assert len(n_c.get_slot("ret").get_links()) == 0
    for link in n_b.get_gate("por").get_links():
        assert link.weight == 0.5


@pytest.mark.engine("dict_engine")
def test_node_netapi_link_with_reciprocal_and_concepts(fixed_nodenet):
    # test linking pipe and concept nodes with reciprocal links
    net, netapi, source = prepare(fixed_nodenet)
    n_head = netapi.create_node("Pipe", None, "Head")

    n_d = netapi.create_node("Concept", None, "D")
    n_e = netapi.create_node("Concept", None, "E")
    netapi.link_with_reciprocal(n_head, n_d, "catexp")
    netapi.link_with_reciprocal(n_d, n_e, "symref")
    assert len(n_d.get_gate("sym").get_links()) == 1
    assert len(n_d.get_slot("gen").get_links()) == 2
    assert len(n_head.get_gate("cat").get_links()) == 1
    assert len(n_head.get_slot("exp").get_links()) == 1


def test_node_netapi_unlink(fixed_nodenet):
    # test completely unlinking a node
    net, netapi, source = prepare(fixed_nodenet)
    n_head = netapi.create_node("Pipe", None, "Head")
    n_a = netapi.create_node("Pipe", None, "A")
    n_b = netapi.create_node("Pipe", None, "B")
    n_c = netapi.create_node("Pipe", None, "C")
    n_d = netapi.create_node("Pipe", None, "D")

    nodes = [n_a, n_b, n_c, n_d]
    for source in nodes:
        for target in nodes:
            netapi.link_with_reciprocal(source, target, "porret")

    netapi.unlink(n_b)

    assert len(n_a.get_slot('por').get_links()) == 3
    assert len(n_b.get_slot('por').get_links()) == 3
    assert len(n_c.get_slot('por').get_links()) == 3
    assert len(n_d.get_slot('por').get_links()) == 3


def test_node_netapi_unlink_specific_link(fixed_nodenet):
    # test removing a specific link
    net, netapi, source = prepare(fixed_nodenet)
    n_head = netapi.create_node("Pipe", None, "Head")
    n_a = netapi.create_node("Pipe", None, "A")
    n_b = netapi.create_node("Pipe", None, "B")
    n_c = netapi.create_node("Pipe", None, "C")
    n_d = netapi.create_node("Pipe", None, "D")

    nodes = [n_a, n_b, n_c, n_d]
    for source in nodes:
        for target in nodes:
            netapi.link_with_reciprocal(source, target, "porret")

    netapi.unlink(n_b, "por", n_c, "por")

    assert len(n_a.get_slot('por').get_links()) == 4
    assert len(n_b.get_slot('por').get_links()) == 4
    assert len(n_c.get_slot('por').get_links()) == 3
    assert len(n_d.get_slot('por').get_links()) == 4


def test_node_netapi_unlink_gate(fixed_nodenet):
    # test unlinking a gate
    net, netapi, source = prepare(fixed_nodenet)
    n_head = netapi.create_node("Pipe", None, "Head")
    n_a = netapi.create_node("Pipe", None, "A")
    n_b = netapi.create_node("Pipe", None, "B")
    n_c = netapi.create_node("Pipe", None, "C")
    n_d = netapi.create_node("Pipe", None, "D")

    nodes = [n_a, n_b, n_c, n_d]
    for source in nodes:
        for target in nodes:
            netapi.link_with_reciprocal(source, target, "porret")

    netapi.unlink(n_b, "por")

    assert len(n_a.get_slot('por').get_links()) == 3
    assert len(n_b.get_slot('por').get_links()) == 3
    assert len(n_c.get_slot('por').get_links()) == 3
    assert len(n_d.get_slot('por').get_links()) == 3


def test_node_netapi_unlink_direction(fixed_nodenet):
    # test unlinking a gate
    net, netapi, source = prepare(fixed_nodenet)
    n_head = netapi.create_node("Pipe", None, "Head")
    n_a = netapi.create_node("Pipe", None, "A")
    n_b = netapi.create_node("Pipe", None, "B")
    n_c = netapi.create_node("Pipe", None, "C")

    netapi.link_with_reciprocal(n_head, n_a, "subsur")
    netapi.link_with_reciprocal(n_head, n_b, "subsur")
    netapi.link_with_reciprocal(n_head, n_c, "subsur")

    nodes = [n_a, n_b, n_c]
    for source in nodes:
        for target in nodes:
            netapi.link_with_reciprocal(source, target, "porret")

    netapi.unlink_direction(n_b, "por")

    assert len(n_head.get_gate('sub').get_links()) == 3
    assert len(n_head.get_slot('sur').get_links()) == 3

    assert len(n_a.get_slot('por').get_links()) == 2
    assert len(n_b.get_slot('por').get_links()) == 0
    assert len(n_c.get_slot('por').get_links()) == 2

    netapi.unlink_direction(n_head, "sub")

    assert len(n_head.get_gate('sub').get_links()) == 0
    assert len(n_head.get_slot('sur').get_links()) == 3

    assert len(n_a.get_slot('sub').get_links()) == 0
    assert len(n_b.get_slot('sub').get_links()) == 0
    assert len(n_c.get_slot('sub').get_links()) == 0


def test_node_netapi_import_actors(fixed_nodenet, test_world):
    # test importing data targets as actors
    net, netapi, source = prepare(fixed_nodenet)
    micropsi.set_nodenet_properties(fixed_nodenet, world_uid=test_world, worldadapter='Braitenberg')
    root_ns = netapi.get_nodespace(None)
    netapi.import_actors(root_ns.uid)
    actors = netapi.get_nodes(root_ns.uid, nodetype="Actor")
    assert len(actors) == 2
    assert set([a.get_parameter('datatarget') for a in actors]) == set(net.worldadapter_instance.datatargets.keys())

    # do it again, make sure we can call import multiple times
    netapi.import_actors(root_ns.uid)
    actors = netapi.get_nodes(root_ns.uid, nodetype="Actor")
    assert len(actors) == 2


def test_node_netapi_import_sensors(fixed_nodenet, test_world):
    # test importing data sources as sensors
    net, netapi, source = prepare(fixed_nodenet)
    micropsi.set_nodenet_properties(fixed_nodenet, world_uid=test_world, worldadapter='Braitenberg')
    root_ns = netapi.get_nodespace(None)
    netapi.import_sensors(root_ns.uid)
    sensors = netapi.get_nodes(root_ns.uid, nodetype="Sensor")
    assert len(sensors) == 2
    assert set([s.get_parameter('datasource') for s in sensors]) == set(net.worldadapter_instance.datasources.keys())

    # do it again, make sure we can call import multiple times
    netapi.import_sensors(root_ns.uid)
    sensors = netapi.get_nodes(root_ns.uid, nodetype="Sensor")
    assert len(sensors) == 2


def test_set_gate_function(fixed_nodenet):
    # test setting a custom gate function
    from micropsi_core.nodenet.gatefunctions import sigmoid
    net, netapi, source = prepare(fixed_nodenet)

    some_other_node_type = netapi.create_node("Pipe", None)
    netapi.unlink(source, "gen")

    net.step()
    assert source.get_gate("gen").activation == 0

    netapi.set_gatefunction(netapi.get_nodespace(None).uid, "Register", "gen", "sigmoid")

    source.set_gate_parameter('gen', 'theta', 1)

    net.step()

    assert round(source.get_gate("gen").activation, 5) == round(sigmoid(0, 0, 1), 5)
    assert some_other_node_type.get_gate("gen").activation == 0


def test_autoalign(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    for uid in net.get_node_uids():
        net.get_node(uid).position = [12, 13, 11]
    netapi.autoalign_nodespace(netapi.get_nodespace(None).uid)
    positions = []
    for uid in net.get_node_uids():
        if net.get_node(uid).parent_nodespace == netapi.get_nodespace(None).uid:
            positions.extend(net.get_node(uid).position)
    assert set(positions) != set([12, 13, 11])

    for uid in net.get_node_uids():
        net.get_node(uid).position = [12, 13, 11]
    netapi.autoalign_nodespace('InVaLiD')
    positions = []
    for uid in net.get_node_uids():
        positions.extend(net.get_node(uid).position)
    assert set(positions) == set([12, 13, 11])


def test_autoalign_updates_last_changed(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    for uid in net.get_node_uids():
        net.get_node(uid).position = [12, 13, 11]
    net.step()
    net.step()
    netapi.autoalign_nodespace(netapi.get_nodespace(None).uid)
    changes = net.get_nodespace_changes([None], 2)
    for uid in net.get_node_uids():
        if net.get_node(uid).position != [12, 13, 11]:
            assert uid in changes['nodes_dirty']


def test_copy_nodes(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    nodespace = netapi.create_nodespace(None, name='copy')
    a1 = netapi.get_node('n0001')
    a2 = netapi.get_node('n0002')
    a1.set_parameter('expecation', 0.6)
    a1.set_gate_parameter('gen', 'amplification', 0.27)
    mapping = netapi.copy_nodes([a1, a2], nodespace.uid)
    assert a1 in mapping
    assert a2 in mapping
    assert a1.name == mapping[a1].name
    assert mapping[a1].parent_nodespace == nodespace.uid
    assert mapping[a2].parent_nodespace == nodespace.uid
    assert set(nodespace.get_known_ids()) == set([mapping[a1].uid, mapping[a2].uid])
    assert len(mapping[a1].get_slot('gen').get_links()) == 0  # incoming link from outside not copied
    assert mapping[a1].get_gate('por').get_links()[0].target_node.uid == mapping[a2].uid
    assert a1.clone_parameters() == mapping[a1].clone_parameters()
    assert a1.get_gate_parameters() == mapping[a1].get_gate_parameters()


def test_group_nodes_by_names(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    sepp1 = netapi.create_node("Register", None, "sepp1")
    sepp2 = netapi.create_node("Register", None, "sepp2")
    sepp3 = netapi.create_node("Register", None, "sepp3")
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")
    seppen_act = netapi.get_activations(None, "sepp")
    assert len(seppen_act) == 3


def test_group_nodes_by_ids(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    ids = ["n0001", "n0002"]
    netapi.group_nodes_by_ids(None, ids, "some")
    some_act = netapi.get_activations(None, "some")
    assert len(some_act) == 2


def test_ungroup_nodes(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    ids = ["n0001", "n0002"]
    netapi.group_nodes_by_ids(None, ids, "some")
    netapi.ungroup_nodes(None, "some")


def test_get_activations(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    sepp1 = netapi.create_node("Register", None, "sepp1")
    sepp2 = netapi.create_node("Register", None, "sepp2")
    sepp3 = netapi.create_node("Register", None, "sepp3")
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")
    seppen_act = netapi.get_activations(None, "sepp")
    assert len(seppen_act) == 3
    assert seppen_act[0] == 0
    assert seppen_act[1] == 0
    assert seppen_act[2] == 0

    netapi.link(source, "gen", sepp2, "gen")
    net.step()

    seppen_act = netapi.get_activations(None, "sepp")
    assert seppen_act[0] == 0
    assert seppen_act[1] == 1
    assert seppen_act[2] == 0


def test_substitute_activations(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    sepp1 = netapi.create_node("Register", None, "sepp1").uid
    sepp2 = netapi.create_node("Register", None, "sepp2").uid
    sepp3 = netapi.create_node("Register", None, "sepp3").uid
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")

    netapi.link(source, "gen", netapi.get_node(sepp2), "gen")
    net.step()

    suddenly_a_wild_activation_appears = [0.2, -1, 42]
    netapi.substitute_activations(None, "sepp", suddenly_a_wild_activation_appears)

    assert round(netapi.get_node(sepp1).get_gate('gen').activation, 2) == 0.2
    assert round(netapi.get_node(sepp2).get_gate('gen').activation, 2) == -1
    assert round(netapi.get_node(sepp3).get_gate('gen').activation, 2) == 42

    netapi.link(netapi.get_node(sepp2), "gen", netapi.get_node(sepp3), "gen")
    net.step()

    seppen_act = netapi.get_activations(None, "sepp")
    assert round(seppen_act[0], 2) == 0
    assert round(seppen_act[1], 2) == 1
    assert round(seppen_act[2], 2) == -1


def test_get_thetas(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    sepp1 = netapi.create_node("Register", None, "sepp1")
    sepp2 = netapi.create_node("Register", None, "sepp2")
    sepp3 = netapi.create_node("Register", None, "sepp3")
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")
    seppen_theta = netapi.get_thetas(None, "sepp")
    assert len(seppen_theta) == 3
    assert seppen_theta[0] == 0
    assert seppen_theta[1] == 0
    assert seppen_theta[2] == 0


def test_set_thetas(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    sepp1 = netapi.create_node("Register", None, "sepp1")
    sepp2 = netapi.create_node("Register", None, "sepp2")
    sepp3 = netapi.create_node("Register", None, "sepp3")
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")

    some_thetas = [1, 2, 3]
    netapi.set_thetas(None, "sepp", some_thetas)

    net.step()

    seppen_theta = netapi.get_thetas(None, "sepp")
    assert round(seppen_theta[0], 2) == 1
    assert round(seppen_theta[1], 2) == 2
    assert round(seppen_theta[2], 2) == 3


def test_get_link_weights(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)

    sepp1 = netapi.create_node("Register", None, "sepp1")
    sepp2 = netapi.create_node("Register", None, "sepp2")
    sepp3 = netapi.create_node("Register", None, "sepp3")
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")

    hugo1 = netapi.create_node("Register", None, "hugo1")
    hugo2 = netapi.create_node("Register", None, "hugo2")
    netapi.group_nodes_by_names(None, node_name_prefix="hugo")

    netapi.link(sepp2, "gen", hugo1, "gen", 0.4)

    w = netapi.get_link_weights(None, "sepp", None, "hugo")
    value = None

    # list style indexing
    try:
        value = round(float(w[0][1]), 2)
    except:
        pass

    # numpy style indexing
    try:
        value = round(float(w[0, 1]), 2)
    except:
        pass

    assert value == 0.4


def test_set_link_weights(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)

    sepp1 = netapi.create_node("Register", None, "sepp1")
    sepp2 = netapi.create_node("Register", None, "sepp2")
    sepp3 = netapi.create_node("Register", None, "sepp3")
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")

    hugo1 = netapi.create_node("Register", None, "hugo1")
    hugo2 = netapi.create_node("Register", None, "hugo2")
    netapi.group_nodes_by_names(None, node_name_prefix="hugo")

    netapi.link(sepp2, "gen", hugo1, "gen", 0.4)

    w = netapi.get_link_weights(None, "sepp", None, "hugo")

    # change value
    # list style indexing
    try:
        w[0][1] = 0.6
    except:
        pass

    # numpy style indexing
    try:
        w[0, 1] = 0.6
    except:
        pass

    netapi.set_link_weights(None, "sepp", None, "hugo", w)
    assert round(float(netapi.get_node(sepp2.uid).get_gate('gen').get_links()[0].weight), 2) == 0.6

    # remove link
    # list style indexing
    try:
        w[0][1] = 0
    except:
        pass

    # numpy style indexing
    try:
        w[0, 1] = 0
    except:
        pass
    netapi.set_link_weights(None, "sepp", None, "hugo", w)
    assert len(netapi.get_node(sepp2.uid).get_gate('gen').get_links()) == 0

    # create link
    # list style indexing
    try:
        w[1][1] = 0.5
    except:
        pass

    # numpy style indexing
    try:
        w[1, 1] = 0.5
    except:
        pass
    netapi.set_link_weights(None, "sepp", None, "hugo", w)
    assert len(netapi.get_node(sepp2.uid).get_gate('gen').get_links()) == 1


def test_get_node_ids(fixed_nodenet):
    net, netapi, source = prepare(fixed_nodenet)
    sepp1 = netapi.create_node("Register", None, "sepp1")
    sepp2 = netapi.create_node("Register", None, "sepp2")
    sepp3 = netapi.create_node("Register", None, "sepp3")
    netapi.group_nodes_by_names(None, node_name_prefix="sepp")
    seppen_ids = netapi.get_node_ids(None, "sepp")
    assert len(seppen_ids) == 3
    assert seppen_ids[0] == sepp1.uid
    assert seppen_ids[1] == sepp2.uid
    assert seppen_ids[2] == sepp3.uid


def test_add_gate_monitor(test_nodenet, node):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    uid = netapi.add_gate_monitor(node, 'gen', name='sepp', color='#987654')
    assert nodenet.get_monitor(uid).name == 'sepp'
    assert nodenet.get_monitor(uid).type == 'gate'
    assert nodenet.get_monitor(uid).color == '#987654'


@pytest.mark.engine("dict_engine")
def test_add_slot_monitor(test_nodenet, node):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    uid = netapi.add_slot_monitor(node, 'gen')
    assert nodenet.get_monitor(uid).type == 'slot'


def test_add_link_monitor(test_nodenet, node):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    uid = netapi.add_link_monitor(node, 'gen', node, 'gen', name='sepplink')
    assert nodenet.get_monitor(uid).name == 'sepplink'
    assert nodenet.get_monitor(uid).property == 'weight'


def test_add_modulator_monitor(test_nodenet):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    nodenet.step()
    uid = netapi.add_modulator_monitor('base_age', 'age')
    assert nodenet.get_monitor(uid).modulator == 'base_age'
    assert nodenet.get_monitor(uid).name == 'age'


def test_add_custom_monitor(test_nodenet):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    function = "return len(netapi.get_nodes())"
    uid = netapi.add_custom_monitor(function, 'number_of_nodes', color=None)
    assert nodenet.get_monitor(uid).name == 'number_of_nodes'
    assert nodenet.get_monitor(uid).function == function


def test_get_monitor(test_nodenet, node):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    uid = netapi.add_gate_monitor(node, 'gen')
    assert nodenet.get_monitor(uid) == netapi.get_monitor(uid)


def test_remove_monitor(test_nodenet, node):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    uid = netapi.add_gate_monitor(node, 'gen')
    netapi.remove_monitor(uid)
    assert nodenet.get_monitor(uid) is None


def test_set_dashboard_value(test_nodenet, node):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    netapi.set_dashboard_value('foo', 'bar')
    assert nodenet.dashboard_values['foo'] == 'bar'


def test_decay_porret_links(test_nodenet):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    pipes = []
    netapi.set_modulator('base_porret_decay_factor', 0.1)
    for i in range(10):
        node = netapi.create_node("Pipe", None, "P%d" % i)
        pipes.append(node)
        if i > 0:
            netapi.link_with_reciprocal(pipes[i - 1], node, 'porret', weight=0.1 * i)

    netapi.link_with_reciprocal(pipes[0], pipes[1], 'subsur', weight=0.5)
    reg = netapi.create_node("Register", None, "source")
    netapi.link(reg, 'gen', pipes[0], 'gen', 0.4)
    netapi.decay_por_links(None)
    for i in range(9):
        assert round(pipes[i].get_gate('por').get_links()[0].weight, 3) == round(0.1 * (i + 1) * 0.9, 3)
    # sub/sur/ret/gen links unchanged
    assert round(reg.get_gate('gen').get_links()[0].weight, 3) == 0.4
    assert round(pipes[0].get_gate('sub').get_links()[0].weight, 3) == 0.5
    assert round(pipes[7].get_gate('ret').get_links()[0].weight, 3) == 0.7


def test_unlink_gate(test_nodenet):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    node = netapi.create_node("Pipe", None)
    pipe1 = netapi.create_node("Pipe", None)
    pipe2 = netapi.create_node("Pipe", None)
    netapi.link_with_reciprocal(node, pipe1, 'subsur')
    netapi.link_with_reciprocal(node, pipe2, 'subsur')
    netapi.link(node, 'por', pipe1, 'gen')
    netapi.link(node, 'por', pipe2, 'gen')
    netapi.link(node, 'por', pipe1, 'sur')
    micropsi.save_nodenet(test_nodenet)
    netapi.unlink_gate(node, 'por')
    assert node.get_gate('por').empty
    assert not node.get_gate('sub').empty
    micropsi.revert_nodenet(test_nodenet)
    netapi = micropsi.nodenets[test_nodenet].netapi
    node = netapi.get_node(node.uid)
    netapi.unlink_gate(node, 'por', target_node_uid=pipe1.uid)
    assert len(node.get_gate('por').get_links()) == 1
    assert node.get_gate('por').get_links()[0].target_node.uid == pipe2.uid
    micropsi.revert_nodenet(test_nodenet)
    netapi = micropsi.nodenets[test_nodenet].netapi
    node = netapi.get_node(node.uid)
    netapi.unlink_gate(node, 'por', target_slot_name='sur')
    assert len(node.get_gate('por').get_links()) == 2  # pipe1:gen, pipe2:gen
    assert len(node.get_gate('sub').get_links()) == 2  # only por->sub unlinked


def test_unlink_slot(test_nodenet):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    node = netapi.create_node("Pipe", None)
    pipe1 = netapi.create_node("Pipe", None)
    pipe2 = netapi.create_node("Pipe", None)
    netapi.link_with_reciprocal(node, pipe1, 'subsur')
    netapi.link_with_reciprocal(node, pipe2, 'subsur')
    netapi.link(pipe1, 'gen', node, 'por')
    netapi.link(pipe2, 'gen', node, 'por')
    netapi.link(pipe1, 'sur', node, 'por')
    micropsi.save_nodenet(test_nodenet)
    netapi.unlink_slot(node, 'por')
    assert node.get_slot('por').empty
    assert not node.get_slot('sur').empty
    micropsi.revert_nodenet(test_nodenet)
    netapi = micropsi.nodenets[test_nodenet].netapi
    node = netapi.get_node(node.uid)
    netapi.unlink_slot(node, 'por', source_node_uid=pipe1.uid)
    assert len(node.get_slot('por').get_links()) == 1
    assert node.get_slot('por').get_links()[0].source_node.uid == pipe2.uid
    micropsi.revert_nodenet(test_nodenet)
    netapi = micropsi.nodenets[test_nodenet].netapi
    node = netapi.get_node(node.uid)
    netapi.unlink_slot(node, 'por', source_gate_name='sur')
    assert len(node.get_slot('por').get_links()) == 2  # pipe1:gen, pipe2:gen
    assert len(node.get_slot('sur').get_links()) == 2  # only sur->por unlinked


def test_nodespace_properties(test_nodenet):
    nodenet = micropsi.get_nodenet(test_nodenet)
    netapi = nodenet.netapi
    rootns = netapi.get_nodespace(None)
    netapi.set_nodespace_properties(None, {'foo': 'bar'})
    data = netapi.get_nodespace_properties()
    assert data[rootns.uid] == {'foo': 'bar'}
