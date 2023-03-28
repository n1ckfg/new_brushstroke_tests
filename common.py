import numpy as np
import trimesh
import pymeshlab as ml
from sklearn.cluster import DBSCAN
from scipy.interpolate import splprep, splev
import sys

def distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)

def map(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def normalizeMesh(vertices):
    magnitudes = np.linalg.norm(vertices, axis=1)
    return vertices / magnitudes[:, np.newaxis]

def loadMesh(inputUrl):
    mesh = trimesh.load(inputUrl)

    try:
        print("Found mesh with " + str(len(mesh.faces)) + " faces.")
    except:
        print("Meshing pointcloud with 0 faces.")
        ms = ml.MeshSet()
        ms.load_new_mesh(inputUrl)
        ms.generate_surface_reconstruction_ball_pivoting()
        #ms.transfer_attributes_per_vertex(sourcemesh=0, targetmesh=1)
        ms.save_current_mesh("temp.ply", save_vertex_color=True)
        mesh = trimesh.load("temp.ply")

    return mesh

def getBounds(mesh):
    bounds = distance(mesh.bounds[0], mesh.bounds[1])
    print("Bounds: " + str(bounds))
    return bounds

def dbscanLines(points, eps=0.1, min_samples=5):
    returns = []

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(points)
    labels = dbscan.labels_

    for label in labels:
        if label == -1: # skip points that belong to no cluster
            continue
        cluster_points = points[labels == label]
        tck, u = splprep(cluster_points.T, s=0)
        new_points = splev(np.linspace(0, 1, 100), tck)
        returns.append(new_points)

    return returns

def voxelize(mesh, dim=128):
    dims = (dim, dim, dim)
    grid = np.zeros(dims)
    
    for point in mesh.vertices:
        x, y, z = point
        ix, iy, iz = int(x / dim), int(y / dim), int(z / dim)
        grid[ix, iy, iz] = 1

    return grid
