import bpy
from bpy_extras import view3d_utils
from mathutils import geometry

camera = bpy.context.scene.camera
cam_matrix = camera.matrix_world.inverted()

cursor_location = bpy.context.scene.cursor.location

area = bpy.context.area
old_type = area.type
area.type = 'VIEW_3D'
cursor_coords = view3d_utils.location_3d_to_region_2d(bpy.context.region, bpy.context.space_data.region_3d, cursor_location)
area.type = old_type

width = bpy.context.scene.render.resolution_x
height = bpy.context.scene.render.resolution_y
ndc_x = (cursor_coords[0] / width - 0.5) * 2.0
ndc_y = (cursor_coords[1] / height - 0.5) * 2.0
ndc = (ndc_x, ndc_y)

ray_origin = cam_matrix @ (0, 0, 0)
ray_direction = cam_matrix @ (ndc[0], ndc[1], 1.0)
ray_direction -= ray_origin
ray_direction.normalize()

hit, location, normal, face_index = geometry.intersect_ray_triangles(ray_origin, ray_direction, mesh.vertices, mesh.polygons)