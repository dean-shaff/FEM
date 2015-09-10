import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D
from triangulate_grid import triangulate

class FEM(object):

    def __init__(self,start, end, hx, hy):
        """
        Initialization creates the mesh for the problem.
        """
        triangles, mesh, boundary, internal, area = triangulate(start, end, hx, hy)
        self.triangles = triangles
        self.mesh = mesh 
        self.boundary = boundary
        self.internal = internal
        self.area = area 


    def adj_triangles(self,node_coord):
        """
        Finds the triangles that are adjacent to a node coordinate
        """
        adj_tri = []
        
        for tri in self.triangles:
            for coord in tri:
                if coord == node_coord:
                    adj_tri.append(tri)
                    break
        return adj_tri

 
    def calc_param(self,tri_coord,node_coord):
        """
        given a set of coordinates of triangle vertices and 
        the coordinates of a node 
        calculate beta and gamma for that piece of basis function
            -tri_coord is the list of coordinates of the triangle on which we're calculating params 
            -node_coord is the coordnates of the node coord around which we're calculating params. 
        """
        x_basis, y_basis = node_coord
        A = []
        for j,coord in enumerate(tri_coord):
            xi, yi = coord 
            A.append([1.0,xi,yi])
            if xi == x_basis and yi == y_basis:
                special = j
                continue 

        b = np.zeros(3,dtype=float)
        b[special] = 1.0

        param = np.linalg.solve(A,b)

        return param[1:] #ignore /alpha because its falls out of gradient

        # print(calc_param((0,1,11),0))

    def M(self,i,j):
        """
        i is the index of the ith basis function (or interior node)
        j is the index of the jth basis function

        calculates the integral of the dot product of the gradients of 
        the ith and jth basis function over the entire domain. 
        """
        node_i = self.internal[i]
        node_j = self.internal[j]
        # x_i, y_i = self.internal[i]
        # x_j, y_j = self.internal[j]
        adj_i = self.adj_triangles(node_i)
        adj_j = self.adj_triangles(node_j)
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
            beta_i, gamma_i = self.calc_param(tri_h,node_i)
            beta_j, gamma_j = self.calc_param(tri_h,node_j)
            total_integral += ((beta_i*beta_j)+(gamma_i*gamma_j))*area_h
            
        return total_integral 

    def solve(self):

        size_internal = len(self.internal)

        M_matrix = [[self.M(i,j) for j in xrange(size_internal)] for i in xrange(size_internal)] 
        print(np.asarray(M_matrix))
        f = 5*np.ones(size_internal) #f is just some constant 
        u_interior = np.linalg.solve(M_matrix,f)
        u_bound = np.zeros(len(self.boundary))
        u = np.hstack((u_bound, u_interior))

        return u 


if __name__ == '__main__':
    solver = FEM([0,0],[5,5],.25,.25)
    u = solver.solve()
    bound, internal = solver.boundary, solver.internal
    mesh = solver.boundary + solver.internal 
    x_mesh, y_mesh = zip(*mesh)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x_mesh, y_mesh, u)
    plt.show()

