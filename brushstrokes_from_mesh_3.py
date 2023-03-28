import trimesh
import numpy as np
from common import *
import latk
from scipy.spatial import Delaunay
from scipy.spatial.distance import cdist

argv = sys.argv[sys.argv.index("--") + 1:] # get all args after "--"
inputPath = argv[0]

la = latk.Latk(init=True)

mesh = trimesh.load(inputPath)
bounds = getBounds(mesh)
searchRadius = bounds * 0.02
minPointsCount = 10
alpha = 0.1
print("Search radius: " + str(searchRadius) + ", Min points per stroke: " + str(minPointsCount))

def get_delaunay_points(mesh, alpha):
	tri = Delaunay(mesh.vertices)
	
	a = tri.points[tri.simplices][:, 0, :]
	b = tri.points[tri.simplices][:, 1, :]
	c = tri.points[tri.simplices][:, 2, :]
	ab = b - a
	ac = c - a
	bc = c - b
	ab_cross_ac = np.cross(ab, ac)
	ab_cross_ac_norm = np.sqrt(np.sum(ab_cross_ac ** 2, axis=1))
	circumradius = ab_cross_ac_norm / (2 * np.sqrt(np.sum(ab ** 2, axis=1)) * np.sqrt(np.sum(ac ** 2, axis=1)) * np.sqrt(np.sum(bc ** 2, axis=1)))
	selected_simplices = tri.simplices[circumradius < alpha]
	
	return tri.points[np.unique(selected_simplices)]

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

points = get_delaunay_points(mesh, alpha)
strokes = group_points_into_strokes(points, searchRadius)

for stroke in strokes:
	la_stroke = latk.LatkStroke()
	for index in stroke:
		vert = mesh.vertices[index]
		la_point = latk.LatkPoint(co=(vert[0], vert[2], vert[1]))
		la_stroke.points.append(la_point)
	la.layers[0].frames[0].strokes.append(la_stroke)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.normalize()
    la.write("output.latk")
else:
    print("No strokes generated.")


