import trimesh
import numpy as np
import latk
from common import *

inputUrl = "untitled.ply"
#inputUrl = "input/input_001_resample.ply"
#inputUrl = "input/TeiyaPrime_000.obj"

la = latk.Latk(init=True)

mesh = loadMesh(inputUrl)

bounds = getBounds(mesh)

max_distance = bounds * 0.1
max_points = 100
skip_points = 4

sharp = mesh.face_adjacency_angles > np.radians(90)
edges = mesh.face_adjacency_edges[sharp]
lines = mesh.vertices[mesh.edges]
#lines = mesh.vertices[mesh.edges_unique]

la_s = latk.LatkStroke()
la_p = latk.LatkPoint(co=lines[0][0])
la_s.points.append(la_p)

for i in range(1, len(lines), skip_points):
    makeNewStroke = False

    new_point = lines[i][0]

    if (len(la_s.points) < max_points):
        last_point = la_s.points[len(la_s.points)-1].co

        if (distance(new_point, last_point) < max_distance):
            la_p = latk.LatkPoint(co=new_point)
            la_s.points.append(la_p)
        else:
            makeNewStroke = True
    else:
        makeNewStroke = True

    if (makeNewStroke == True):
        for la_p in la_s.points:
            la_p.co = [la_p.co[0], la_p.co[2], la_p.co[1]]

        la.layers[0].frames[0].strokes.append(la_s)
        la_s = latk.LatkStroke()
        la_p = latk.LatkPoint(co=new_point)
        la_s.points.append(la_p)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.write("output.latk")
else:
    print("No strokes generated.")


