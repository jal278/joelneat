#include "evolve.h"
double bigbuff[LARGESX*LARGESY];
double coordarray[10][SX*SY*4];

PyObject *to_array(double* buffer,int sx, int sy) {
  int offset=0;
  PyObject* ret = PyList_New(sy);
   for(int y=0;y<sy;y++) {
    PyObject *row = PyList_New(sx);
    for(int x=0;x<sx;x++) {
      PyList_SetItem(row,x,PyFloat_FromDouble(buffer[offset]));
      offset++;
    }
    PyList_SetItem(ret,y,row);
   }
  return ret;
}

void init_coordarray()
 {
 double theta=0.0;
 for(int x=0;x<6;x++) 
    create_coordarray(coordarray[x],SX,SY,0.0); //x*6.28/6);	
}

void initialize() {
	init_coordarray();
}
/*
 void artist::optimize(evaluator* e) {
  double oldscore = e->evaluate_artist(this);
  mutate_buffer();
  double newscore = e->evaluate_artist(this);
  if(oldscore>newscore)
   undo_mutate_buffer();
 }

 void artist::optimize(feature_evaluator* e) {
  double oldscore = e->evaluate_artist(this);
  mutate_buffer();
  double newscore = e->evaluate_artist(this);
  if(oldscore>newscore)
   undo_mutate_buffer();
 }
*/
