import numpy as np
from sklearn.cluster import DBSCAN
from scipy.interpolate import splprep, splev
import latk
from pyntcloud import PyntCloud

def load_point_cloud(file_path):
    cloud = PyntCloud.from_file(file_path)
    points = cloud.points.values
    print("Loaded point cloud with " + str(len(points)) + " points.")
    return points

def cluster_points(points, eps=4.0, min_samples=10):
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    print("Found " + str(len(clustering.labels_)) + " clusters.")
    return clustering.labels_

def generate_polylines(points, labels):
    unique_labels = set(labels)
    polylines = []

    for label in unique_labels:
        if label == -1: # -1 is noise in DBSCAN            
            continue

        cluster_points = points[labels == label]

        # Fit a curve to each cluster
        tck, u = splprep([cluster_points[:, 0], cluster_points[:, 1], cluster_points[:, 2]], s=0)
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new, z_new = splev(u_new, tck, der=0)
        polylines.append(np.vstack([x_new, y_new, z_new]).T)

    return polylines

point_cloud = load_point_cloud("elephant.ply")
labels = cluster_points(point_cloud)
polylines = generate_polylines(point_cloud, labels)
print(polylines)

la = latk.Latk(init=True)

for polyline in polylines:
    la_stroke = latk.LatkStroke()
    for point in polyline:
        la_point = latk.LatkPoint(co=(point[0], point[2], point[1]))
        la_stroke.points.append(la_point)
    la.layers[0].frames[0].strokes.append(la_stroke)

if (len(la.layers[0].frames[0].strokes) > 0):
    la.normalize()
    print(str(len(la.layers[0].frames[0].strokes)) + " strokes generated.")
    la.write("output.latk")
else:
    print("No strokes generated.")
