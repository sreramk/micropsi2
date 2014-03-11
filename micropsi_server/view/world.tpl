

<div class="sectionbar">
    <form class="navbar-form">
        <table width="100%">
            <tr>
                <td>
                    <table>
                        <tr>
                            <td><span data-toggle="collapse" data-target="#world_editor"><i
                                    class="icon-chevron-right"></i></span></td>

                             <td>
                                <div class="btn-group" id="world_list">
                                    %include nodenet_list type="world",mine=mine,others=others,current=current
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
                <td>
                    <table class="pull-right">
                        <tr>
                            <td style="white-space:nowrap;">
                                <div class="btn-group">
                                  <a href="#" id="world_reset" class="btn"><i class="icon-fast-backward"></i></a>
                                  <a href="#" id="world_start" class="btn"><i class="icon-play"></i></a>
                                  <a href="#" id="world_step_forward" class="btn"><i class="icon-step-forward"></i></a>
                                  <a href="#" id="world_stop" class="btn"><i class="icon-pause"></i></a>
                                </div>
                            </td>

                            <td align="right"><input id="world_step" type="text" disabled="disabled"
                                                     style="text-align:right; width:60px;" value="0"/></td>

                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </form>
</div>

<div id="world_editor" class="section-margin collapse in">
    <div class="section">
        <div class="editor_field span9">
            <canvas id="world" width="700" height="500" style="background:#eeeeee"></canvas>
        </div>
        <div class="editor_field " id="world_forms">
            <form class="form-horizontal">
                <h4>World Status</h4>
                <textarea disabled="disabled" id="world_status" rows="4" cols="60" class="input-xlarge"></textarea>
            </form>
            <form class="form-horizontal" id="world_objects">
                <h4>Agents</h4>
                <div id="world_agents_list">
                    <table class="table-striped table-condensed"></table>
                </div>
                <h4>World Objects</h4>
                <div id="world_objects_list">
                    <a href="#" id="add_object_link" class="add_link">+ add Object</a>
                    <table class="table-striped table-condensed"></table>
                </div>
                <div id="world_objects_icons" style="visibility:hidden;"></div>
            </form>

            <form class="form-horizontal hide" id="edit_worldobject">
                <h4>World Object</h4>
                <table class="table-condensed">
                    <tr>
                        <td><label for="wo_uid_input">Uid</label></td>
                        <td><input type="text" class="" name="wo_uid" id="wo_uid_input" /></td>
                    </tr>
                    <tr>
                        <td><label for="wo_name_input">Name</label></td>
                        <td><input type="text" class="" name="wo_name" id="wo_name_input" /></td>
                    </tr>
                    <tr>
                        <td><label for="wo_type">Type</label></td>
                        <td><select type="text" class="" name="wo_type" id="wo_type_input"></select></td>
                    </tr>
                    <tr>
                        <td><label>Parameters</label></td>
                        <td class="wo_parameters"><table id="wo_parameter_list"></table>
                            <button id="add_object_param">Add parameter</button></td>
                    </tr>
                </table>
                <div class="controls">
                    <button type="reset" class="btn">Cancel</button>
                    <button type="submit" class="btn btn-primary">Apply</button>
                </div>
            </form>

        </div>
    </div>
</div>

<div class="dropdown" id="create_object_menu">
    <a class="dropdown-toggle" data-toggle="dropdown" href="#create_object_menu"></a>
    <ul class="world_menu dropdown-menu">
        <li><a href="#" data="add_worldobject">Add worldobject</a></li>
    </ul>
</div>


%if world_js:
    <script src="/static/{{world_js}}" type="text/paperscript" canvas="world"></script>
