import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D

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


def plot_tri_mesh():
    for tri in triangles:
        tri_x = []
        tri_y = []
        tri = list(tri)
        tri.append(tri[0])
        for index in tri:
            tri_x.append(x_mesh[index])
            tri_y.append(y_mesh[index])
    #     tri_x.append(x_mesh[tri[0]])
    #     tri_y.append(y_mesh[tri[0]])
        plt.plot(tri_x,tri_y)
        
    plt.plot(x_mesh[:2],y_mesh[:2])
    plt.scatter(x_mesh,y_mesh);
    
# plot_tri_mesh()



def adj_triangles(interior_index):
    x_i, y_i = x_mesh_interior[interior_index], y_mesh_interior[interior_index]
    adj_tri = []
    
    for tri in triangles:
        for index in tri:
            if x_mesh[index] == x_i and y_mesh[index] == y_i:
                adj_tri.append(tri)
                break
    return adj_tri

def tri_area(coord):
    """
    given a set of coordinates (of indices of mesh points),
    calculate the area of the triangle. 
    """
    xy_coord = []
    sides = [] 
    xi, yi = x_mesh[0], x_mesh[0]
    coord_new = list(coord)
    coord_new.append(coord[0])
    for i in coord_new[1:]:
        xi_new, yi_new = x_mesh[i], y_mesh[i] 
        sides.append(np.sqrt((xi-xi_new)**2 + (yi-yi_new)**2))
        xi, yi = xi_new, yi_new
        xy_coord.append([xi,yi])
    a, b, c = sides 
#     print(a,b,c)
    x = (b**2 + c**2 - a**2)/(2.0*b*c)
    return (c*b*np.sqrt(np.absolute(1.0-x**2)))/2.0

# for i in xrange(len(triangles)):
#     print(tri_area(triangles[i]))
# print(tri_area(triangles[2]))

def calc_param(coord,i):
    """
    given a set of coordinates (of indices of mesh points),
    calculate beta and gamma for that piece of basis function
    i is the index of the basis function 
    """
    x_basis, y_basis = x_mesh_interior[i], y_mesh_interior[i]
    A = []
    for j,index in enumerate(coord):
        xi, yi = x_mesh[index], y_mesh[index]
        A.append([1.0,xi,yi])
        if xi == x_basis and yi == y_basis:
            special = j
            continue 
    
    b = np.zeros(3,dtype=float)
    b[special] = 1.0
    
    param = np.linalg.solve(A,b)
    
    return param[1:] #ignore /alpha because its falls out of gradient

# print(calc_param((0,1,11),0))

def M(i,j):
    """
    i is the index of the ith basis function (or interior node)
    j is the index of the jth basis function
    
    calculates the integral of the dot product of the gradients of 
    the ith and jth basis function over the entire domain. 
    """
    x_i, y_i = x_mesh_interior[i], y_mesh_interior[j]
    x_j, y_j = x_mesh_interior[i],y_mesh_interior[j]
    adj_i = adj_triangles(i)
    adj_j = adj_triangles(j)
    shared_tri = [] 
    for tri_i in adj_i:
        for tri_j in adj_j:
            if tri_i == tri_j:
                shared_tri.append(tri_i)
                break 
    total_integral = 0.0
    for tri_h in shared_tri:
#         area_h = tri_area(tri_h)
        area_h = 0.5 #for this problem
        beta_i, gamma_i = calc_param(tri_h,i)
        beta_j, gamma_j = calc_param(tri_h,j)
        total_integral += ((beta_i*beta_j)+(gamma_i*gamma_j))*area_h
        
    return total_integral 

M_matrix = [[M(i,j) for j in xrange(len(x_mesh_interior))] for i in xrange(len(x_mesh_interior))] 
f = 5*np.ones(len(x_mesh_interior)) #f is just some constant 
u_interior = np.linalg.solve(M_matrix,f)
u_bound = np.zeros(len(x_mesh_bound))
u = np.hstack((u_bound, u_interior))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(x_mesh, y_mesh, u)
plt.show()

