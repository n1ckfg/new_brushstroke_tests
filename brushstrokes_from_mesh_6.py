import numpy as np
from scipy.spatial import KDTree
import latk
from pyntcloud import PyntCloud

num_neighbors = 2

def load_point_cloud(file_path):
    cloud = PyntCloud.from_file(file_path)
    points = cloud.points.values
    print("Loaded point cloud with " + str(len(points)) + " points.")
    return points

def generate_polylines(points, num_neighbors=2):
    tree = KDTree(points) 
    
    distances, indices = tree.query(points, k=num_neighbors + 1) # Find the nearest neighbors for each point

    polylines = [] 
    for i, neighbors in enumerate(indices):
        for neighbor in neighbors:
            if neighbor != i: 
                #polyline = sorted([points[i], points[neighbor]]) 
                polyline = tuple(sorted([i, neighbor]))
                if polyline not in polylines: 
                    polylines.append(polyline)

    return polylines

point_cloud = load_point_cloud("input/untitled007.ply")
polylines = generate_polylines(point_cloud, num_neighbors)

la = latk.Latk(init=True)

for polyline in polylines:
    la_stroke = latk.LatkStroke()
    for index in polyline:
        point = point_cloud[index]
        la_point = latk.LatkPoint(co=(point[0], point[2], point[1]))
        la_stroke.points.append(la_point)
    la.layers[0].frames[0].strokes.append(la_stroke)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.normalize()
    print(str(len(la.layers[0].frames[0].strokes)) + " strokes generated.")
    la.write("output.latk")
else:
    print("No strokes generated.")
