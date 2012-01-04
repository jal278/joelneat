#ifndef SOLVEMAZE
#define SOLVEMAZE
extern int sx,sy,ex,ey;
vector<float> solve_maze2(int* m,int width,int height,int& steps,vector<int>* path,int startx,int starty,int endx, int endy);
vector<float> solve_maze(int* m,int width,int height,int& steps,vector<int>* points,int startx,int starty,int endx, int endy);
#endif
