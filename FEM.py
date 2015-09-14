import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D
from triangulate_grid import triangulate, triangulate_hole, plot_tri_array

class FEM(object):

    def __init__(self, start, end, hx, hy, hole_start, hole_end):
        """
        Initialization creates the mesh for the problem.
        """
        mesh, boundary, internal, triangles = triangulate_hole(start, end, hx, hy, hole_start, hole_end)
        self.triangles = triangles
        self.mesh = mesh 
        self.boundary = boundary
        self.internal = internal
        self.area = (hx*hy)/2.0
        self.hx, self.hy = hx,hy

    def adj_triangles(self,node_coord):
        """
        Finds the triangles that are adjacent to a node coordinate
        """
        node_index = self.internal.index(node_coord)
        adj_tri = self.triangles[node_index]

        return adj_tri
        # adj_tri = []
        
        # for tri in self.triangles:
        #     if node_coord in tri:
        #         adj_tri.append(tri)
        # # adj_tri = self.internal_dict[str(self.internal.index(node_coord))]
        # return adj_tri

        # return self.adj_triangle_dict[str(node_coord)]

 
    def calc_param(self,tri_coord,node_coord):
        """
        given a set of coordinates of triangle vertices and 
        the coordinates of a node 
        calculate beta and gamma for that piece of basis function
            -tri_coord is the list of coordinates of the triangle on which we're calculating params 
            -node_coord is the coordinates of the node coord around which we're calculating params. 
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
        adj_i = self.adj_triangles(node_i)
        adj_j = self.adj_triangles(node_j)
        shared_tri = [] 
        for tri_i in adj_i:
            for tri_j in adj_j:
                if sorted(tri_i) == sorted(tri_j):
                    shared_tri.append(tri_i)
                    break 

        # print(len(shared_tri))


        total_integral = 0.0
        for tri_h in shared_tri:
            beta_i, gamma_i = self.calc_param(tri_h,node_i)
            beta_j, gamma_j = self.calc_param(tri_h,node_j)
            total_integral += ((beta_i*beta_j)+(gamma_i*gamma_j))*self.area 
            
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
    solver = FEM([0,0],[5,5],.5,.5,[0,0],[2,2])
    u = solver.solve()
    bound, internal = solver.boundary, solver.internal
    mesh = solver.boundary + solver.internal 
    x_mesh, y_mesh = zip(*mesh)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x_mesh, y_mesh, u)
    plt.show()










