#include "display_cppn.h"
#include <math.h>

#define NOISYPIC


void create_coordarray(double* coordarray,int sx,int sy,double theta) {
 int offset=0;
 double coordinate[4]={-1.0,-1.0,-1.0,1.0};
 double dx= 2.0/sx;
 double dy= 2.0/sy;

 for (int y=0;y<sy;y++) {
      for (int x=0;x<sx;x++) {
        coordinate[2] = sqrt(coordinate[0]*coordinate[0]+coordinate[1]*coordinate[1]);    
	double cos_theta= cos(theta);
 	double sin_theta= sin(theta);
        double newx = coordinate[0]*cos_theta-coordinate[1]*sin_theta;
	double newy = coordinate[0]*sin_theta+coordinate[1]*cos_theta;
	for (int k=0;k<4;k++)
         coordarray[k] = coordinate[k];
        coordarray[0]=newx;
	coordarray[1]=newy;
     coordarray+=4;
     coordinate[0]+=dx;
     }
     coordinate[0] = -1.0;
     coordinate[1] += dy;

     }
}
void gen_buffer_opt(double* buf, CPPN* c,double* coordarray,int arraysize)
{
for(int x=0;x<arraysize;x++)
{
 double val=(c->query_net(coordarray)+1.0)/2.0;
#ifdef NOISYPIC
val+=randfloat()*0.2-0.1;
#endif
 buf[x]=val;
 coordarray+=4;


}

}

int gen_buffer(double* buf, CPPN* c,int sx, int sy)
{
 int offset=0;
 double coordinate[4]={-1.0,-1.0,-1.0,1.0};
 double dx= 2.0/sx;
 double dy= 2.0/sy;

 int outputs=c->outputs.size();
     for (int y=0;y<sy;y++) {
      for (int x=0;x<sx;x++) {
      coordinate[2] = sqrt(coordinate[0]*coordinate[0]+coordinate[1]*coordinate[1]);    
     buf[offset] = (c->query_net(coordinate)+1.0)/2.0;

     offset++;
     coordinate[0]+=dx;
     }
     coordinate[0] = -1.0;
     coordinate[1] += dy;

     }
}
