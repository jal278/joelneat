#include "display_cppn.h"
#include <math.h>
int gen_buffer(double* buf, CPPN* c,int sx, int sy)
{
 int offset=0;
 double coordinate[3]={-1.0,-1.0,-1.0};
 double dx= 2.0/sx;
 double dy= 2.0/sy;

 int outputs=c->outputs.size();
     for (int y=0;y<sy;y++) {
      for (int x=0;x<sx;x++) {
      //coordinate[2] = sqrt(coordinate[0]*coordinate[0]+coordinate[1]*coordinate[1]);    
     buf[offset] = absd(c->query_net(coordinate));

     offset++;
     coordinate[0]+=dx;
     }
     coordinate[0] = -1.0;
     coordinate[1] += dy;

     }
}
