bl_info = {
	"name": "Camera Array Generator",
	"author": "Savvas S",
	"version": (0, 1),
	"blender": (4, 2, 0),
	"location": "View3D > Sidebar > Camera Array Generator",
	"description": "Generates an array of cameras on the faces of the selected object",
	"warning": "",
	"doc_url": "",
	"category": "Object",
}

import bpy
import bmesh
from mathutils import Vector

class CameraArrayGeneratorPanel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Camera Array Generator"
	bl_idname = "OBJECT_PT_camera_array_generator"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Camera Array Generator"

	def draw(self, context):
		layout = self.layout

		obj = context.object

		row = layout.row()
		row.prop(obj, "focal_length")

		row = layout.row()
		row.operator("object.generate_camera_array")

class GenerateCameraArrayOperator(bpy.types.Operator):
	"""Generates an array of cameras on the faces of the selected object"""
	bl_idname = "object.generate_camera_array"
	bl_label = "Generate Camera Array"

	def execute(self, context):
		
		focal_length = 50  # Change this value to set the focal length

		obj = bpy.context.active_object

		bpy.ops.object.mode_set(mode='OBJECT')

		mesh = bpy.data.meshes.new("CameraTargets")

		target_obj = bpy.data.objects.new("CameraTargets", mesh)

		bpy.context.collection.objects.link(target_obj)

		bm = bmesh.new()
		bm.from_mesh(obj.data)

		target_locations = []

		for face in bm.faces:
			# Calculate the center of the face
			center = face.calc_center_median()
			target_locations.append(center)

		bm.free()

		mesh.from_pydata(target_locations, [], [])
		mesh.update()

		for vert in mesh.vertices:
			camera_data = bpy.data.cameras.new(name='Camera')
			camera_obj = bpy.data.objects.new('Camera', camera_data)

			camera_data.lens = focal_length

			bpy.context.collection.objects.link(camera_obj)

			camera_obj.location = vert.co

			direction = -vert.co.normalized()
			rotation = direction.to_track_quat('-Z', 'Y')
			camera_obj.rotation_euler = rotation.to_euler()

		obj.select_set(True)
		bpy.context.view_layer.objects.active = obj

		bpy.ops.object.mode_set(mode='EDIT')

		bpy.ops.mesh.select_all(action='SELECT')

		bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

		bpy.context.scene.render.use_multiview = True
		bpy.context.scene.render.views_format = 'MULTIVIEW'
		bpy.context.scene.render.views["left"].use = False
		bpy.context.scene.render.views["right"].use = False

		for i, obj in enumerate(bpy.data.objects):
			if obj.type == 'CAMERA' and obj.name.startswith("Camera"):
				obj.data.stereo.convergence_mode = 'PARALLEL'

				view = bpy.context.scene.render.views.new(obj.name)

				if i == 0:
					view.camera_suffix = ""
				else:
					view.camera_suffix = ".{:03d}".format(i)


		bpy.ops.object.editmode_toggle()
		bpy.ops.object.select_all(action='DESELECT')
		ob = bpy.context.scene.objects["CameraTargets"]
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.view_layer.objects.active = ob
		ob.select_set(True)
		bpy.ops.object.select_pattern(pattern="Camera*")
		bpy.context.view_layer.objects.active = obj
		obj.select_set(True)
		bpy.ops.object.parent_set(type='OBJECT')
		bpy.context.object.hide_render = True
		return {'FINISHED'}

def register():
	bpy.utils.register_class(CameraArrayGeneratorPanel)
	bpy.utils.register_class(GenerateCameraArrayOperator)
	bpy.types.Object.focal_length = bpy.props.FloatProperty(name="Focal Length", default=50.0)

def unregister():
	bpy.utils.unregister_class(CameraArrayGeneratorPanel)
	bpy.utils.unregister_class(GenerateCameraArrayOperator)
	del bpy.types.Object.focal_length

if __name__ == "__main__":
	register()
