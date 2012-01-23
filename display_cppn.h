#ifndef DCPN
#define DCPN
/*This source code copyrighted by Lazy Foo' Productions (2004-2009) and may not
be redestributed without written permission.*/

//Include SDL functions and datatypes
#include "hneat.h"
int gen_buffer(double* buf, CPPN* c,int sx, int sy);
int threshold_buffer(double * buf,int sx, int sy); 
void create_coordarray(double* coordarray,int sx,int sy,double theta);
void gen_buffer_opt(double* buf, CPPN* c,double* coordarray,int arraysize);
#endif
