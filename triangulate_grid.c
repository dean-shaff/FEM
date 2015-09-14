#include <stdio.h>

//triangulate grid

int main(){
	float start[2] = {0.0, 0.0}; 
	float end[2] = {5.0,5.0};
	float hx = 1.0; 
	float hy = 1.0;
	triangulate(start, end, hx, hy)	;
	return 1; 
}

