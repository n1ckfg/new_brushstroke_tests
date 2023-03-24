import trimesh
import pymeshlab as ml
import numpy as np
import latk
from common import *

argv = sys.argv[sys.argv.index("--") + 1:] # get all args after "--"
inputPath = argv[0]

la = latk.Latk(init=True)

mesh = loadMesh(inputPath)

bounds = getBounds(mesh)

# generate a set of contour lines at regular intervals
interval = bounds * 0.01 #0.03  #0.1 # the spacing between contours
print("Interval: " + str(interval))

# x, z
slice_range = np.arange(mesh.bounds[0][2], mesh.bounds[1][2], interval)
# y
#slice_range = np.arange(mesh.bounds[0][1], mesh.bounds[0][2], interval)

# loop over the z values and generate a contour at each level
for slice_pos in slice_range:
    # x
    #slice_mesh = mesh.section(plane_origin=[slice_pos, 0, 0], plane_normal=[1, 0, 0])
    # y
    #slice_mesh = mesh.section(plane_origin=[0, slice_pos, 0], plane_normal=[0, 1, 0])
    # z
    slice_mesh = mesh.section(plane_origin=[0, 0, slice_pos], plane_normal=[0, 0, 1])
    
    if slice_mesh != None:
        for entity in slice_mesh.entities:
            la_s = latk.LatkStroke()

            for index in entity.points:
                vert = slice_mesh.vertices[index]
                vert = [vert[0], vert[2], vert[1]]
                la_p = latk.LatkPoint(co=vert)
                la_s.points.append(la_p)

            la.layers[0].frames[0].strokes.append(la_s)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.normalize()
    la.write("output.latk")
else:
    print("No strokes generated.")

