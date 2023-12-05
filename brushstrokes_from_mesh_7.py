import numpy as np
from scipy.spatial import Delaunay
import latk
import trimesh

mesh = trimesh.load("input/elephant.ply")
la = latk.Latk(init=True)

points = mesh.vertices

tri = Delaunay(points[:, :2])

threshold_distance = 0.2

lines = []

def are_points_close(point1, point2, threshold):
    distance = np.linalg.norm(point1 - point2)
    return distance <= threshold

# Iterate through each triangle in the Delaunay triangulation
for simplex in tri.simplices:
    triangle_vertices = points[simplex]

    current_line = []

    for vertex in triangle_vertices:
        is_close_to_existing_point = any(are_points_close(vertex, p, threshold_distance) for p in current_line)

        if is_close_to_existing_point:
            current_line.append(vertex)
        else:
            # If the current vertex is too far from any existing point, start a new line
            if current_line:
                lines.append(np.array(current_line))
            current_line = [vertex]

    # Add the last line (if any) to the list of lines
    if current_line:
        lines.append(np.array(current_line))

for line in lines:
    la_stroke = latk.LatkStroke()
    for point in line:
        la_point = latk.LatkPoint(co=(point[0], point[2], point[1]))
        la_stroke.points.append(la_point)
    la.layers[0].frames[0].strokes.append(la_stroke)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.normalize()
    print(str(len(la.layers[0].frames[0].strokes)) + " strokes generated.")
    la.write("output.latk")
else:
    print("No strokes generated.")
