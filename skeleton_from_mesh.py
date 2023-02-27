import trimesh
import skeletor as sk
import pymeshlab as ml
import numpy as np
import latk
from common import *

inputUrl = "input/input.ply"
#inputUrl = "input/input_001_resample.ply"
#inputUrl = "input/TeiyaPrime_000.obj"

la = latk.Latk(init=True)

mesh = loadMesh(inputUrl)

fixed = sk.pre.fix_mesh(mesh, remove_disconnected=5, inplace=False)
skel = sk.skeletonize.by_wavefront(fixed, waves=1, step_size=1)

for entity in skel.skeleton.entities:
    la_s = latk.LatkStroke()

    for index in entity.points:
        vert = skel.vertices[index]
        vert = [vert[0], vert[2], vert[1]]
        la_p = latk.LatkPoint(co=vert)
        la_s.points.append(la_p)

    la.layers[0].frames[0].strokes.append(la_s)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.write("output.latk")
else:
    print("No strokes generated.")

