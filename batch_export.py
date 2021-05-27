"""
Script by Albert Ortiz @skydrowDev 
Automatically bakes and exports all the actions of a control rig/game rig workflow.
"""

import bpy

"""
-------------------------
    GLOBAL PARAMETERS
-------------------------
"""
control_rig_name = 'rig'
game_rig_name = 'root'
prefix = 'prefix_'
export_folder = 'Test/'     #Relative to the .blend directory
batch_export = True         #False if you only want to bake/export the current action, otherwise bakes all actions

#Switches to pose mode and selects all the game rig's bones
def SelectGameRigBones():
    obj2.select_set(state=True)
    bpy.context.view_layer.objects.active = obj2
    bpy.ops.object.mode_set(mode='POSE')
    for a in bpy.context.visible_pose_bones:
        a.bone.select = True  

#Returns a list with the action's frame range [FrameStart, FrameEnd]
def GetActionFrameRange(action):
    keys = (sorted(set([item for item in action.frame_range])))
    return keys

#Initialization
obj = bpy.data.objects[control_rig_name] #Control rig
obj2 = bpy.data.objects[game_rig_name] #Game rig
ad = obj.animation_data
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

#Iterates over all the control rig's actions
if ad and ad.action:
    for t in ad.nla_tracks:
        for s in t.strips:
            #Action baking
            obj.select_set(state=True)
            ad.action = s.action
            SelectGameRigBones()
            lastFrame = GetActionFrameRange(ad.action)[1]
            op_state = bpy.ops.nla.bake(
                frame_end = lastFrame,
                use_current_action = False,
                only_selected = True,
                visual_keying = True,
                clear_constraints = False,
                clear_parents = True,
                clean_curves = True,
                bake_types={'POSE'}
                )       
            action_name = '{0}{1}'.format(prefix, s.action.name)
            obj2.animation_data.action.name = action_name

            #Action fbx export
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            obj2.select_set(state=True)
            bpy.ops.export_scene.fbx(
                filepath = bpy.path.abspath('//{0}{1}.fbx'.format(export_folder, action_name)),
                use_selection = True,
                object_types = {'ARMATURE', 'MESH'},
                mesh_smooth_type = 'FACE',
                add_leaf_bones = False,
                use_armature_deform_only = True,
                bake_anim = True,
                )
        if(not batch_export):
            break
