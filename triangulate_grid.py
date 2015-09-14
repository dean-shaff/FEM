import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

def triangulate_hole(start,end,hx,hy,hole_start,hole_end):
	"""
	-start is a tuple (or list) containing coordinates of start position
	-end is a tuple (or list) containing coordinates of end position 
	-hx and hy are the size of the side of each triangle (a measure of how fine mesh is)
		in x and y direction respectively 
	-hole_start 
	-hole_end is list containing coor
	"""	
	area = (hx*hy)/2.0
	L_init = [start,[start[0]+hx,start[1]],[start[0],start[1]+hy]]
	U_init = [[start[0]+hx,start[1]],[start[0],start[1]+hy],[start[0]+hx,start[1]+hy]]
	diff_y = end[1] - start[1]
	diff_x = end[0] - start[0]
	mesh = []
	boundary = [] 
	internal = [] 
	for x in xrange(int(diff_x / hx)+1):
		for y in xrange(int(diff_y / hy)+1):
			grid_x = start[0] + (x*hx)
			grid_y = start[1] + (y*hx)
			if (grid_x <= hole_start[0] or grid_x >= hole_end[0] or 
				grid_y <= hole_start[1] or grid_y >= hole_end[1]):
				mesh.append([grid_x,grid_y])
				if (grid_y >= hole_start[1] and grid_y <= hole_end[1] and
					grid_x >= hole_start[0] and grid_x <= hole_end[0]):
					boundary.append([grid_x, grid_y])
				elif (grid_y == start[1] or grid_y == end[1] or 
					grid_x == start[0] or grid_x == end[0] and [grid_x, grid_y] not in boundary):
					boundary.append([grid_x, grid_y])
				else:
					internal.append([grid_x,grid_y])
	triangles = [] 
	for coord in internal:
		a, b = coord[0], coord[1]
		tri1 = [[a,b],[a+hx,b-hy],[a,b-hy]]
		tri2 = [[a,b],tri1[-1],[a-hx,b]]
		tri3 = [[a,b],tri2[-1],[a-hx,b+hy]]
		tri4 = [[a,b],tri3[-1],[a,b+hy]]
		tri5 = [[a,b],tri4[-1],[a+hx,b]]
		tri6 = [[a,b],tri5[-1],[a+hx,b-hy]]
		triangles.append([tri1,tri2,tri3,tri4,tri5,tri6])

	return mesh, boundary, internal, triangles 
		


def triangulate(start, end, hx, hy):
	"""
	start is a tuple (or list) containing coordinates of start position
	end is a tuple (or list) containing coordinates of end position 
	hx and hy are the size of the side of each triangle (a measure of how fine mesh is)
		in x and y direction respectively 
	"""
	# if (end[1] - start[1]) % hy != 0 and (end[0] - start[0]) % hx:
	# 	print("Error, can't create mesh")
	area = (hx*hy)/2.0
	diff_y = end[1] - start[1]
	diff_x = end[0] - start[0]
	L_init = [start,[start[0]+hx,start[1]],[start[0],start[1]+hy]]
	U_init = [[start[0]+hx,start[1]],[start[0],start[1]+hy],[start[0]+hx,start[1]+hy]]
	triangles = []
	mesh = [[start[0]+(x*hx), start[1]+(y*hy)] for x in xrange(int(diff_x / hx)+1) for y in xrange(int(diff_y / hy)+1)]
	boundary = []
	internal = [] 
	for coord in mesh: 
		if coord[0] == start[0] or coord[0] == end[0]:
			boundary.append(coord)
		elif coord[1] == start[1] or coord[1] == end[1]:
			boundary.append(coord)
		else:
			internal.append(coord)

	internal_dict = {str(x):[] for x in xrange(len(internal))}
	# adj_triangles = {}
	for x in xrange(int(diff_x / hx)):
		inc_x = x*hx
		for y in xrange(int(diff_y / hy)):
			inc_y = y*hy
			L_next_y = [[coord[0]+inc_x,coord[1]+inc_y] for coord in L_init]
			U_next_y = [[coord[0]+inc_x,coord[1]+inc_y] for coord in U_init]
			for coord_L, coord_U in zip(L_next_y,U_next_y):
				# if coord_L in internal:
				try:
					index = internal.index(coord_L)
					internal_dict[str(index)].append(L_next_y)
					# elif coord_U in internal:						
					index = internal.index(coord_U)
					internal_dict[str(index)].append(U_next_y)
				except ValueError as e:
					continue
					# print(e)
			triangles.extend((L_next_y, U_next_y))

	return triangles, mesh, boundary, internal, area, internal_dict#adj_triangles 

def plot_mesh(mesh):
	"""
	mesh is a list of [x,y] coordinates. 
	"""
	fig = plt.figure(figsize=(16,9))
	ax = fig.add_subplot(111)
	x_mesh = [coord[0] for coord in mesh]
	y_mesh = [coord[1] for coord in mesh]
	ax.scatter(x_mesh,y_mesh)
	plt.show()


def plot_tri_mesh(*args):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	triangles, mesh, boundary, internal, area, adj = triangulate(*args)
	print(triangles[0])
	for tri in triangles:
		tri_new = tri + [tri[0]]
		# print(tri_new)
		x_y = zip(*tri_new)

		ax.plot(x_y[0],x_y[1])
		tri_x = [corner[0] for corner in tri_new]
		tri_y = [corner[1] for corner in tri_new]
		ax.plot(tri_x, tri_y)
	x_mesh = [coord[0] for coord in mesh]
	y_mesh = [coord[1] for coord in mesh]
	ax.scatter(x_mesh,y_mesh)
	plt.show()	
	# triangles_ex = [[tri + tri[0]] for tri in triangles]
	# for tri in triangles_ex:

def plot_tri_array(array,ax):
	"""
	array is an array containing six triangles. 
	ax is the matplotlib axis object 
	"""
	for tri in array:
		tri_new = tri + [tri[0]]
		tri_x = [corner[0] for corner in tri_new]
		tri_y = [corner[1] for corner in tri_new]
		ax.plot(tri_x,tri_y)


if __name__ == '__main__':
	mesh, boundary, internal, triangles  = triangulate_hole([0,0],[10,10],.5,.5,[0,0],[0,0])
	fig = plt.figure(figsize=(16,9))
	ax = fig.add_subplot(111)
	plot_tri_array(triangles[5],ax)
	plt.show()
	plot_mesh(mesh)
	plot_mesh(boundary)
	plot_mesh(internal)




	# triangles, mesh, boundary, internal, area, adj_triangles = triangulate([0,0],[5,5],1,1)
	# plot_tri_mesh([0,0],[5,5],1,1)
	# num = 1 
	# adj1 = []
	# print(adj1)		
	# triangles1 = adj_triangles[str(num)]
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# for tri in triangles1:
	# 	print(tri)
	# 	tri_new = tri + [tri[0]]
	# 	# print(tri_new)
		# x_y = zip(*tri_new)

		# ax.plot(x_y[0],x_y[1])
	# 	tri_x = [corner[0] for corner in tri_new]
	# 	tri_y = [corner[1] for corner in tri_new]
	# 	ax.plot(tri_x, tri_y)
	# plt.show()
	# print(adj_triangles['[0.0,0.0]'])
	# plot_tri_mesh([0,0],[5,5],.1,.1)









