bl_info = {
	"name": "Apply Scale and Resize Modifiers",
	"author": "Kenetics",
	"version": (0, 2),
	"blender": (2, 80, 0),
	"location": "View3D > Apply Object Transform Menu (Ctrl + A)",
	"description": "Applies object scale and applies scale to modifiers.",
	"warning": "",
	"wiki_url": "",
	"category": "Modifiers"
}

import bpy
from bpy.props import EnumProperty, BoolProperty
from bpy.types import Operator, Panel, AddonPreferences

## Helper Functions

def get_real_users(datablock):
	return datablock.users - 1 if datablock.use_fake_user else datablock.users

## Operators

class SA_OT_apply_scale_resize_modifiers(Operator):
	"""Applies object scale and resizes object's modifiers"""
	bl_idname = "object.sa_ot_apply_scale_resize_modifiers"
	bl_label = "Apply Scale and Resize Modifiers"
	bl_options = {'REGISTER','UNDO'}
	
	# Properties
	scale_source : EnumProperty(
		items=[
			("0","X","","",0),
			("1","Y","","",1),
			("2","Z","","",2)
			],
		name="Resize Source",
		description="Which axis to get resize scale for modifiers from.",
		default="0"
	)
	
	duplicate_multi_user_textures : BoolProperty(
		name="Duplicate Multi-User Textures",
		description="Duplicate textures that have multiple users.",
		default=True
	)

	@classmethod
	def poll(cls, context):
		return context.selected_objects

	def execute(self, context):
		for obj in context.selected_objects:
			# get which scale to use from XYZ
			scale = obj.scale[int(self.scale_source)]
			
			if get_real_users(obj.data) > 1:
				obj.data = obj.data.copy()
			
			for mod in obj.modifiers:
				if mod.type == "ARRAY":
					for i in range(3):
						mod.constant_offset_displace[i] *= obj.scale[i]
				elif mod.type == "BEVEL":
					mod.width *= scale
				elif mod.type == "SOLIDIFY":
					mod.thickness *= scale
				elif mod.type == "WIREFRAME":
					mod.thickness *= scale
				elif mod.type == "CAST":
					mod.radius *= scale
					mod.size *= scale
				elif mod.type == "DISPLACE":
					mod.strength *= scale
					# Check if displace mode is not UV, and that texture is assigned
					if mod.texture_coords != "UV" and mod.texture is not None:
						# Check if texture is procedural
						if mod.texture.type in ["CLOUDS", "DISTORTED_NOISE", "MAGIC", "MUSGRAVE", "STUCCI", "VORONOI"]:
							if get_real_users(mod.texture) > 1 and self.duplicate_multi_user_textures:
								mod.texture = mod.texture.copy()
							mod.texture.noise_scale *= scale
						
				elif mod.type == "HOOK":
					mod.falloff_radius *= scale
				elif mod.type == "WAVE":
					mod.start_position_x *= scale
					mod.start_position_y *= scale
					mod.falloff_radius *= scale
					mod.width *= scale
					mod.height *= scale
					mod.narrowness /= scale
					
		
		# Apply scale to selected objects
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

		return {'FINISHED'}

## Append to UI Helper Functions

def add_apply_scale_resize_modifiers_button(self, context):
	self.layout.operator(SA_OT_apply_scale_resize_modifiers.bl_idname)

## Register

def register():
	bpy.utils.register_class(SA_OT_apply_scale_resize_modifiers)
	bpy.types.VIEW3D_MT_object_apply.append(add_apply_scale_resize_modifiers_button)

def unregister():
	bpy.types.VIEW3D_MT_object_apply.remove(add_apply_scale_resize_modifiers_button)
	bpy.utils.unregister_class(SA_OT_apply_scale_resize_modifiers)

if __name__ == "__main__":
	register()

