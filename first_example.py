import numpy as np 

x_mesh_bound = np.asarray([1,0,0,1,2,3,4,5,4,3,2])
y_mesh_bound = np.asarray([1,2,3,4,4,4,3,2,1,1,2])
x_mesh_interior = np.asarray([1,1,2,3,4,3])
y_mesh_interior = np.asarray([2,3,3,3,2,2])
x_mesh = np.hstack((x_mesh_bound, x_mesh_interior))
y_mesh = np.hstack((y_mesh_bound, y_mesh_interior))
mesh = zip(x_mesh,y_mesh); 
triangles = [(0,1,11),
            (11,1,2),
            (11,2,12),
            (12,2,3),
            (13,3,4),
            (13,12,3),
            (10,12,13),
            (10,11,12),
            (10,0,11),
            (14,4,5),
            (14,13,4),
            (16,13,14),
            (16,10,13),
            (9,10,16),
            (6,14,5),
            (15,14,6),
            (15,16,14),
            (8,16,15),
            (8,9,16),
            (7,15,6),
            (7,8,15)] 