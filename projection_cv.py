import cv2
import numpy as np
import trimesh

K = np.array([[1000, 0, 500], [0, 1000, 500], [0, 0, 1]]).astype(np.float32) 
R = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]).astype(np.float32) 
t = np.array([[0,], [0,], [0,]]).astype(np.float32)

R, _ = cv2.Rodrigues(R)

mesh = trimesh.load("input.ply")
point_cloud = mesh.vertices

proj_points, _ = cv2.projectPoints(point_cloud, R, t, K, None)

img = np.zeros((1000, 1000, 3), dtype=np.uint8)

for i in range(proj_points.shape[0]):
    x, y = proj_points[i][0][0], proj_points[i][0][1]
    cv2.circle(img, (int(x), int(y)), 2, (0, 0, 255), -1)

cv2.imshow('Point Cloud', img)
cv2.waitKey(0)