import trimesh
import pymeshlab as ml
import numpy as np
import latk
from scipy.spatial.distance import cdist
from common import *

argv = sys.argv[sys.argv.index("--") + 1:] # get all args after "--"
inputPath = argv[0]

la = latk.Latk(init=True)

ms = ml.MeshSet()
ms.load_new_mesh(inputPath)
mesh = ms.current_mesh()
bounds = mesh.bounding_box().diagonal()

samplePercentage = 1.0
searchRadius = bounds * 0.05
minPointsCount = 5

newSampleNum = int(mesh.vertex_number() * samplePercentage)
if (newSampleNum < 1):
    newSampleNum = 1

try:
    ms.transfer_texture_to_color_per_vertex(sourcemesh=0, targetmesh=0)     
    print("Found texture, converting to vertex color.")
except:
    print("No texture found.")

# The resample method can subtract points from an unstructured point cloud, 
# but needs connection information to add them.
if (samplePercentage > 1.0):
    if (mesh.edge_number() == 0 and mesh.face_number() == 0):
        ms.generate_surface_reconstruction_ball_pivoting()
    ms.generate_sampling_poisson_disk(samplenum=newSampleNum, subsample=False)
    ms.transfer_attributes_per_vertex(sourcemesh=0, targetmesh=1)
else:
    ms.generate_sampling_poisson_disk(samplenum=newSampleNum, subsample=True)

mesh = ms.current_mesh()

print("Search radius: " + str(searchRadius) + ", Min points per stroke: " + str(minPointsCount))

def group_points_into_strokes(points, radius):
    strokes = []
    unassigned_points = set(range(len(points)))

    while len(unassigned_points) > 0:
        stroke = [next(iter(unassigned_points))]
        unassigned_points.remove(stroke[0])

        for i in range(len(points)):
            if i in unassigned_points and cdist([points[i]], [points[stroke[-1]]])[0][0] < radius:
                stroke.append(i)
                unassigned_points.remove(i)

        if (len(stroke) >= minPointsCount):
        	strokes.append(stroke)
        print("Found " + str(len(strokes)) + " strokes, " + str(len(unassigned_points)) + " points remaining.")
    return strokes

strokes = group_points_into_strokes(mesh.vertex_matrix(), searchRadius)

for stroke in strokes:
	la_stroke = latk.LatkStroke()
	for index in stroke:
		vert = mesh.vertex_matrix()[index]
		la_point = latk.LatkPoint(co=(vert[0], vert[2], vert[1]))
		la_stroke.points.append(la_point)
	la.layers[0].frames[0].strokes.append(la_stroke)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.normalize()
    la.write("output.latk")
else:
    print("No strokes generated.")


