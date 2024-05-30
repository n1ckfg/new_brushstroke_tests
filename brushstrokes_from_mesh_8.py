import open3d as o3d
import numpy as np
from scipy.spatial import KDTree
from collections import defaultdict
import matplotlib.pyplot as plt

default_distance_threshold = 0.02

def load_point_cloud(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    return pcd

def segment_point_cloud(pcd, distance_threshold=default_distance_threshold):
    points = np.asarray(pcd.points)
    tree = KDTree(points)
    clusters = defaultdict(list)
    visited = set()

    def region_grow(point_idx):
        cluster = []
        stack = [point_idx]
        while stack:
            idx = stack.pop()
            if idx not in visited:
                visited.add(idx)
                cluster.append(idx)
                neighbors = tree.query_ball_point(points[idx], distance_threshold)
                stack.extend(neighbors)
        return cluster

    for i in range(len(points)):
        if i not in visited:
            cluster = region_grow(i)
            if len(cluster) > 1:  # Ignore small clusters
                clusters[len(clusters)] = cluster

    return clusters

def create_polylines(clusters, points, distance_threshold=default_distance_threshold):
    polylines = []
    for i, cluster in enumerate(clusters.values()):
        cluster_points = points[cluster]
        cluster_tree = KDTree(cluster_points)
        start_idx = cluster_tree.query(cluster_points.mean(axis=0))[1]
        polyline = [cluster_points[start_idx]]
        visited = {start_idx}

        for _ in range(len(cluster_points) - 1):
            try:
                current_idx = cluster_tree.query(polyline[-1])[1]
                neighbors = cluster_tree.query_ball_point(polyline[-1], r=distance_threshold)
                next_idx = min((idx for idx in neighbors if idx not in visited), key=lambda idx: np.linalg.norm(cluster_points[idx] - polyline[-1]))
                visited.add(next_idx)
                polyline.append(cluster_points[next_idx])
            except:
                pass
        
        if (len(polyline) > 1):  
            print("Built polyline " + str(i+1) + " of " + str(len(clusters.values())) + " with " + str(len(polyline)) + " points.")
            polylines.append(np.array(polyline))
    return polylines

def visualize_polylines(polylines):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for polyline in polylines:
        ax.plot(polyline[:, 0], polyline[:, 2], polyline[:, 1])
    plt.show()

if __name__ == "__main__":
    file_path = "input_010.ply"
    
    print("Loading point cloud: " + file_path)
    pcd = load_point_cloud(file_path)

    print("")

    print("Clustering points...")
    clusters = segment_point_cloud(pcd, distance_threshold=default_distance_threshold)
    print("Found " + str(len(clusters)) + " clusters.")

    print("")
    
    print("Building polylines...")
    points = np.asarray(pcd.points)
    polylines = create_polylines(clusters, points)
    print("Created " + str(len(polylines)) + " polylines.")
    
    visualize_polylines(polylines)
