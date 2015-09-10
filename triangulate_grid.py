import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

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

	for x in xrange(int(diff_x / hx)):
		inc_x = x*hx
		for y in xrange(int(diff_y / hy)):
			inc_y = y*hy
			L_next_y = [[coord[0]+inc_x,coord[1]+inc_y] for coord in L_init]
			U_next_y = [[coord[0]+inc_x,coord[1]+inc_y] for coord in U_init]
			new_coord = [start[0]+inc_x, start[1]+inc_y]
			# mesh.append(new_coord)
			triangles.extend((L_next_y, U_next_y))

	return triangles, mesh, boundary, internal, area  



def plot_tri_mesh(*args):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	triangles, mesh, boundary, internal = triangulate(*args)
	# print(triangles[0])
	# for tri in triangles:
	# 	tri_new = tri + [tri[0]]
	# 	# print(tri_new)
	# 	x_y = zip(*tri_new)

	# 	ax.plot(x_y[0],x_y[1])
		# tri_x = [corner[0] for corner in tri_new]
		# tri_y = [corner[1] for corner in tri_new]
		# ax.plot(tri_x, tri_y)
	x_mesh = [coord[0] for coord in boundary]
	y_mesh = [coord[1] for coord in boundary]
	ax.scatter(x_mesh,y_mesh)
	plt.show()	
	# triangles_ex = [[tri + tri[0]] for tri in triangles]
	# for tri in triangles_ex:




if __name__ == '__main__':
	plot_tri_mesh([0,0],[5,5],.1,.1)
