bl_info = {
    "name" : "Graph Channel Filter",
    "author" : "TarkanV",
    "version" : "001",
    "description" : "Allows to filter and focus on a specific F-Curves. ",
    "blender" : (2, 83, 0),
    "location" : "Graph Editor -> Right Panel",
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
    
    tfrm = bpy.props.StringProperty()
    #bpy.ops.wm.context_set_enum(data_path="area.type", value="GRAPH_EDITOR")
    def execute(self, context):
        #if(bpy.context.space.type == 'DOPESHEET_EDITOR'):
        #bpy.ops.wm.context_set_enum(data_path="area.type", value="GRAPH_EDITOR")
        print(bpy.context.space_data.type)
        bpy.context.space_data.dopesheet.filter_text = self.tfrm;
        
        bpy.ops.anim.channels_select_all(action='SELECT')
        key = context.scene.focus.keyfocus
        if(key):
            bpy.ops.graph.view_selected()
        else:
            bpy.ops.graph.view_all()
            bpy.ops.graph.view_frame()
        
        
        
        
        
        return {'FINISHED'}
        
    


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
        ting = bpy.props.BoolProperty()
        col.prop(tool, "keyfocus", text="Focus On Selected")
        
        row = layout.row()
        row.operator('pick.op', text = "Loc").tfrm = "Location"
        row = layout.row()
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "X Location"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "Y Location"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "Z Location" 
        
        row = layout.row()
        row.operator('pick.op', text = "Rot").tfrm = "Rotation"
        row = layout.row()
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "X Euler"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "Y Euler"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "Z Euler"
        
        row = layout.row()
        row.operator('pick.op', text = "Scale").tfrm = "Scale"
        row = layout.row()
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "X Scale"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "Y Scale"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "Z Scale" 
'''      
class DopesheetFilter(Panel):
    bl_idname = 'curve.filte2r'
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
        row.operator('pick.op', text = "Loc").tfrm = "Location"
        row = layout.row()
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "X Location"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "Y Location"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "Z Location" 
        
        row = layout.row()
        row.operator('pick.op', text = "Rot").tfrm = "Rotation"
        row = layout.row()
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "X Euler"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "Y Euler"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "Z Euler"
        
        row = layout.row()
        row.operator('pick.op', text = "Scale").tfrm = "Scale"
        row = layout.row()
        row.operator('pick.op', text = "X", icon='KEYTYPE_EXTREME_VEC').tfrm = "X Scale"
        row.operator('pick.op', text = "Y", icon='KEYTYPE_JITTER_VEC').tfrm = "Y Scale"
        row.operator('pick.op', text = "Z", icon='KEYTYPE_BREAKDOWN_VEC').tfrm = "Z Scale" 
        
'''
        
def register():
    bpy.utils.register_class(PickOp)
    bpy.utils.register_class(GraphFilter)
#    bpy.utils.register_class(DopesheetFilter)
    bpy.utils.register_class(FilterProperties)
    bpy.types.Scene.focus = PointerProperty(type=FilterProperties)
    

def unregister():
    bpy.utils.unregister_class(PickOp)
    bpy.utils.unregister_class(GraphFilter)
#    bpy.utils.unregister_class(DopesheetFilter)
    bpy.utils.unregister_class(FilterProperties)
    del bpy.types.Scene.focus
    

if __name__ == "__main__":    
    register()