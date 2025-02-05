bl_info = {
    "name" : "Graph Channel Filter",
    "author" : "TarkanV",
    "version" : "0.1",
    "description" : "Allows to filter and focus on one more F-Curves. ",
    "blender" : (4, 3, 0),
    "location" : "Graph Editor -> Right Panel -> Graph+",
    "warning" : "",
    "category" : "Animation"
    }

import bpy
from bpy.types import Panel, Operator

from bpy.props import (
        BoolProperty,
        StringProperty,
        PointerProperty,
        )
class FilterProperties(bpy.types.PropertyGroup):
    keyfocus: BoolProperty(
        name="Keyframes Focus",
        description="Tick to focus on keyframes only.",
        default=False
    )

class PickOp(Operator):
    bl_idname = 'pick.op'
    bl_label = 'Pick Operator'
    
    isol : bpy.props.BoolProperty()
    tfrm : bpy.props.StringProperty()
    

    
    
    #bpy.ops.wm.context_set_enum(data_path="area.type", value="GRAPH_EDITOR")
    def execute(self, context):
        #if(bpy.context.space.type == 'DOPESHEET_EDITOR'):
        #bpy.ops.wm.context_set_enum(data_path="area.type", value="GRAPH_EDITOR")
        #print(bpy.context.space_data.type)
        
        data = bpy.context.active_object.animation_data
 #     try:    
        transforms = data.action.fcurves
                     
        for  transform in transforms:
            i = 0
            print("\n\n\n******Data path :" + transform.data_path + "\n\n\n")
            bone_name = ""
            if("\"" in transform.data_path):
                bone_name = transform.data_path.split("\"")[1]
                print(f'Bone Name  : {bone_name}')
                selected_bones = bpy.context.selected_pose_bones_from_active_object
                if bone_name in bpy.context.active_object.pose.bones :
                    if(bpy.context.active_object.pose.bones[bone_name] in selected_bones):                
                        if(self.isol == True):
                            transform.hide = True 
                
                print("Data pass : " + transform.data_path)
                if('].' in transform.data_path):
                    path = transform.data_path.split('].')[1]
                    print("Path :" + path)
                    
                    tid = (str(path) + "." + str(transform.array_index))


                    if (tid in str(self.tfrm)):
                        transform.hide = False
            else:
                bone_name = transform.data_path
                #data = bpy.context.active_object.animation_data
                   
                transforms = data.action.fcurves
                print ("Ce code a continué malgré tout in despite ofent :)")             
                for  transform in transforms:
                    if(self.isol == True):
                        transform.hide = True 
                    tid = (str(transform.data_path) + "." + str(transform.array_index))
                    print("\n\n\n******Data path :" + tid + "\n\n\n")
                    print (self.tfrm)
                    if (tid in str(self.tfrm)):
                        
                        transform.hide = False                
            
   #   except:
    #    self.report({'INFO'}, 'This object has no attributed action.')     

        #bpy.context.space_data.dopesheet.filter_text = self.tfrm;
        
        bpy.ops.anim.channels_select_all(action='SELECT')
        key = context.scene.focus.keyfocus
        if(key):
            bpy.ops.graph.view_selected()
        else:
            '''
            types = {'VIEW_3D', 'GRAPH_EDITOR', 'DOPESHEET_EDITOR', 'NLA_EDITOR', 'IMAGE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'TEXT_EDITOR', 'NODE_EDITOR'}
            area = bpy.context.area.type
            for type in types:
                #set the context
                bpy.context.area.type = type

                #print out context where operator works (change the ops below to check a different operator)
                if bpy.ops.graph.view_all.poll():
                    print("This is working on : " + type) 
              '''  
            bpy.ops.graph.view_all()
            bpy.ops.graph.view_frame()    
        
        return {'FINISHED'}
    
    def invoke (self, context, event):
        '''
        if(context.space_data.type == 'DOPESHEET_EDITOR'):        
            bpy.ops.wm.context_set_enum(data_path="area.type", value="GRAPH_EDITOR")
        '''    
            
            
        if (event.shift == False):
            self.isol = True
        else:
            self.isol = False
        
        return self.execute(context)     
        
    


class GraphFilter(Panel):
    bl_idname = 'curve.filter'
    bl_label = "Channel Filter"
    bl_space_type = 'GRAPH_EDITOR'
    
    # bl_space_type = props.space_type_pref()
    bl_region_type = 'UI'
    bl_category = 'Graph+'
    

    def draw(self, context):
        scene = context.scene
        tool = scene.focus 

        layout = self.layout

        row = layout.row(align=True) 
        
        col = layout.column()
        ting : bpy.props.BoolProperty()
        col.prop(tool, "keyfocus", text="Focus On Selected")
        
        row = layout.row()
        rotX = "rotation_axis_angle.0, rotation_quaternion.0, rotation_euler.0"
        rotY = "rotation_axis_angle.1, rotation_quaternion.1, rotation_euler.1"
        rotZ = "rotation_axis_angle.2, rotation_quaternion.2, rotation_euler.2"
        locs = "location.0,location.1,location.2"
        
        rots = rotX + rotY + rotZ + "rotation_quaternion.3" + "rotation_axis_angle.3"
        scals = "scale.0,scale.1,scale.2"
        row.operator('pick.op', text = "Reset", icon='FILE_REFRESH').tfrm = locs+","+rots+","+scals
        
        row = layout.row()
        row.operator('pick.op', text = "Loc").tfrm = locs
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "location.0"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "location.1"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "location.2" 
        
        row = layout.row()
        row.operator('pick.op', text = "Rot").tfrm = rots
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = rotX
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = rotY
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = rotZ
        
        row = layout.row()
        row.operator('pick.op', text = "Scale").tfrm = scals
        
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "scale.0"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "scale.1"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "scale.2" 
 
'''    
class DopesheetFilter(Panel):
    bl_idname = 'curve.filter2'
    bl_label = "Curve Filter"
    bl_space_type = 'DOPESHEET_EDITOR'
    
    # bl_space_type = props.space_type_pref()
    bl_region_type = 'UI'
    bl_category = 'Graph+'
    

    def draw(self, context):
        scene = context.scene
        tool = scene.focus 

        layout = self.layout

        row = layout.row(align=True) 
        
        col = layout.column()
        ting = bpy.props.BoolProperty()
        col.prop(tool, "keyfocus", text="Focus On Selected")
        
        row = layout.row()
        locs = "location.0,location.1,location.2"
        rots = "rotation_euler.0,rotation_euler.1,rotation_euler.2"
        scals = "scale.0,scale.1,scale.2"
        row.operator('pick.op', text = "Reset", icon='FILE_REFRESH').tfrm = locs+","+rots+","+scals
        
        row = layout.row()
        row.operator('pick.op', text = "Loc").tfrm = locs
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "location.0"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "location.1"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "location.2" 
        
        row = layout.row()
        row.operator('pick.op', text = "Rot").tfrm = rots
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "rotation_euler.0"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "rotation_euler.1"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "rotation_euler.2"
        
        row = layout.row()
        row.operator('pick.op', text = "Scale").tfrm = scals
        
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "scale.0"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "scale.1"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "scale.2" 
'''        

        
def register():
    bpy.utils.register_class(PickOp)
    bpy.utils.register_class(GraphFilter)
   # bpy.utils.register_class(DopesheetFilter)
    bpy.utils.register_class(FilterProperties)
    bpy.types.Scene.focus = PointerProperty(type=FilterProperties)
    

def unregister():
    bpy.utils.unregister_class(PickOp)
    bpy.utils.unregister_class(GraphFilter)
   # bpy.utils.unregister_class(DopesheetFilter)
    bpy.utils.unregister_class(FilterProperties)
    del bpy.types.Scene.focus
    

if __name__ == "__main__":    
    register()