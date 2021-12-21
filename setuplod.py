import bpy
from bpy.props import IntProperty

bl_info = {
    "name": "Unity LOD Tool",
    "blender": (2,90,0),
    "author": "Daniel Oberbauer <danieloberbauer@gmail.com>",
    "category": "Object",
    "version": (1,0),
    "description":"Adds LODs with renaming masks for Unity",
    "location": "Object menu",
    }

class SetupLOD (bpy.types.Operator):
    """Addon to set up LOD groups for Unity"""
    bl_idname = "object.setup_lod"
    bl_label = "Set up LOD for Unity"
    bl_options = {'REGISTER', 'UNDO'}
    amount: bpy.props.IntProperty(
        name = "Amount",
        description= "Number of LODs",
        default=3,
        min=1, soft_max=10,
        )
    def execute(self, context):
        C = bpy.context
        src_obj = bpy.context.active_object
        for i in range (0,self.amount-1):
            new_obj = src_obj.copy()
            new_obj.data = src_obj.data.copy()
            new_obj.animation_data_clear()
            C.collection.objects.link(new_obj)
        number = 0
        ratio = 1
        for obj in bpy.context.selected_objects:
            obj.name += "_LOD" + str(number)
            number += 1
            modifier = obj.modifiers.new(name = "Decimate", type = 'DECIMATE')
            modifier.ratio = ratio
            ratio -= 1/self.amount
        return {'FINISHED'}
def menu_func(self, context):
    self.layout.operator(SetupLOD.bl_idname)
def register():
    print("Hello world")
    bpy.utils.register_class(SetupLOD)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    print("Goodbye world")
    bpy.utils.unregister_class(SetupLOD)
#if __name__ == "__main__":
#    register()
