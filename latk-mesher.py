import numpy as np
import trimesh
from shapely.geometry import Polygon
import latk
import math

la = latk.Latk("test.latk")
la_layer = la.layers[0]
print("Loaded latk.")

sweep_radius=0.02
sweep_sides = 4
sweep_polygon_points = np.array([(sweep_radius * math.cos(i * math.pi / (sweep_sides/2)), sweep_radius * math.sin(i * math.pi / (sweep_sides/2))) for i in range(sweep_sides)])
sweep_polygon = Polygon(sweep_polygon_points)

contraction_val = 0.5
smoothing_val = 0.5
smoothing_iterations = 20

for i, la_frame in enumerate(la_layer.frames):
	mesh = trimesh.base.Trimesh()
	
	for la_stroke in la_frame.strokes:
		points = []
		
		for la_point in la_stroke.points:
			co = la_point.co
			points.append([co[0], co[2], co[1]])
		
		points = np.array(points)

		stroke_mesh = trimesh.creation.sweep_polygon(sweep_polygon, path=points, cap_ends=True)
		try:
			trimesh.smoothing.filter_humphrey(stroke_mesh, alpha=contraction_val, beta=smoothing_val, iterations = smoothing_iterations)
		except:
			print("Stroke smooth pass failed.")
			
		vertices = np.concatenate((mesh.vertices, stroke_mesh.vertices))
		faces = np.concatenate((mesh.faces, stroke_mesh.faces + len(mesh.vertices)))
		mesh = trimesh.Trimesh(vertices, faces)

	try:
		trimesh.smoothing.filter_humphrey(mesh, alpha=contraction_val, beta=smoothing_val, iterations = smoothing_iterations)
	except:
		print("Frame smooth pass failed.")
		
	mesh.export("output/test" + str(i) + ".ply")
	print("Saved mesh " + str(i+1) + " of " + str(len(la_layer.frames)))
