#ifndef EVOLVEH
#define EVOLVEH

#include <vector>
#include <algorithm>
#include <time.h>
using namespace std;
#include <Python.h>
#include "hneat.h"
#include "display_cppn.h"
#include "tinyxml/tinyxml.h"
#define SX 64
#define SY 64

#define LARGESX 512
#define LARGESY 512
#include <bzlib.h>
#include <gsl/gsl_statistics.h>
#include <gsl/gsl_sort.h>
#include <gsl/gsl_wavelet.h>
#include <gsl/gsl_wavelet2d.h>

class evaluator;

extern double bigbuff[LARGESX*LARGESY];
class artist {
public:
 bool rendered;
 bool isrendered() { return rendered; }
 double buffer[SX*SY];
 void clear_picture() {
  for (int i=0;i<SX*SY;i++)
   buffer[i]=0.0;
 }
 bool get_nanflag() {
  return orig->nanflag;
 }
 static void random_seed() {
  srand ( time(NULL) );
 }

 int complexity() {
  return orig->complexity();
 }
 const char* save_xml() {
  return orig->save_xml();
 }

 static artist* load_xml(const char* xml_string) {
  artist* newart=new artist();
  delete newart->orig;
  newart->orig= CPPN::load_xml(xml_string);
  return newart;
 }
 static artist* load(const char *fname) {
  artist* k = new artist(CPPN::load(fname));
  return k;
 }
 
 void save(const char *fname) {
  orig->save(fname);
 }
 void load_new(const char *fname) {
  delete orig;
  orig = CPPN::load(fname);
 }

 CPPN* orig;
 Substrate *s,*t;
 artist() {
        rendered=false;
        vector<int> r1;
	vector<int> r2;
	r1.push_back(1);
	r1.push_back(1);
	r1.push_back(1);
	r1.push_back(1);
        s = new Substrate(r1,true,false,false,0);
	t = new Substrate(r2,false,true,false,1);
        orig= new CPPN(s,t,10,false);
        orig->change();
 }
 artist(CPPN* cppn) {
  rendered=false;
  orig=cppn;
 }

 artist* copy() {
  artist* new_art= new artist();
  delete new_art->orig;
  vector<Substrate*> sv;
  sv.push_back(new_art->s);
  sv.push_back(new_art->t);
  new_art->orig=(CPPN*)this->orig->Copy(sv);
  return new_art;
 }

 void mutate() {
  orig->mutate(); 
 }
 void make_random() {
  orig->make_random();
 }

 void change() {
  orig->change();
 }

 PyObject *get_picture() {
  int offset=0;
  PyObject* ret = PyList_New(SY);
   for(int y=0;y<SY;y++) {
    PyObject *row = PyList_New(SX);
    for(int x=0;x<SX;x++) {
      PyList_SetItem(row,x,PyFloat_FromDouble(buffer[offset]));
      offset++;
    }
    PyList_SetItem(ret,y,row);
   }
  return ret;
 }

 PyObject *get_big() {
  int offset=0;
  PyObject* ret = PyList_New(LARGESY);
   for(int y=0;y<LARGESY;y++) {
    PyObject *row = PyList_New(LARGESX);
    for(int x=0;x<LARGESX;x++) {
      int val = (int)(bigbuff[offset]*255.0);
      PyList_SetItem(row,x,PyInt_FromLong(val));
      //PyList_SetItem(row,x,PyFloat_FromDouble(bigbuff[offset]));
      offset++;
    }
    PyList_SetItem(ret,y,row);
   }
  return ret;
 }

 double* render_big() {
  gen_buffer(bigbuff,orig,LARGESX,LARGESY);
  return bigbuff;
 }

 double* render_picture() {
  rendered=true;
  gen_buffer(buffer,orig,SX,SY);
  return buffer; 
 }

 ~artist() {
  delete orig;
  delete s;
  delete t;
 } 
};

class evaluator {
 Network* net;
 public:
 evaluator* copy() {
  evaluator* new_eval = new evaluator();
  delete new_eval->net;
  new_eval->net = this->net->Copy();
  return new_eval; 
 }
 void save(const char* fn) {
  net->save(fn);
 }
 void load(const char* fn) {
  delete net;
  net = Network::load(fn);
 }
 int complexity()  {
  return net->complexity();
 }
 evaluator() {
        vector<int> r1;
	vector<int> r2;
        vector<int> hid;
	r1.push_back(SX);
	r1.push_back(SY);
        hid.push_back(SX/8);
        hid.push_back(SY/8);
        Substrate* s = new Substrate(r1,true,false,false,0);
        Substrate* h = new Substrate(hid,false,false,false,1);
	Substrate* t = new Substrate(r2,false,true,false,2);
        Substrate* b = new Substrate(r2,false,false,true,3);
        //CPPN* orig= new CPPN(s,t,10,true);
        CPPN* orig= new CPPN(s,h,10,true);
        CPPN* orig2= new CPPN(h,t,10,true);
        CPPN* bias= new CPPN(b,h,Singleton::next_inno());
        vector<Substrate*> v1;
        vector<CPPN*> v2;
        v1.push_back(s);
        v1.push_back(b);
        v1.push_back(h);
        v1.push_back(t);
       // t->in_conn.push_back(orig);
       // s->out_conn.push_back(orig);
       // t->in_conn.push_back(bias);
       // b->out_conn.push_back(bias);
        v2.push_back(orig);
        v2.push_back(orig2);
        v2.push_back(bias);
        net = new Network(v1,v2);
 }
 void mutate() {
  net->mutate();
 }
 double evaluate_artist(artist* a) {
  cout << "loading inputs" << endl;
  net->inputs[0]->load_in(a->buffer);
  cout << "activating" << endl;
  for(int k=0;k<2;k++)
   net->activate();
  cout << "done" <<endl;
  return net->outputs[0]->activation;
 }

 ~evaluator() {
  delete net;
 }
};

class feature_detector {
public:
static double average(artist* a) { 
return gsl_stats_mean(a->buffer,1,SX*SY);
} 
static double std(artist* a) {
return gsl_stats_sd(a->buffer,1,SX*SY);
}
static double skew(artist* a) { 
return gsl_stats_skew(a->buffer,1,SX*SY);
}
static double kurtosis(artist* a) { 
return gsl_stats_kurtosis(a->buffer,1,SX*SY);
}

static double std_block(double* buffer,int x, int y, int size)
{
double block[400];
int count=0;
for(int i=0;i<size;i++)
 for(int j=0;j<size;j++)
  block[count++]=buffer[i*SX+j];
return gsl_stats_sd(block,1,size*size);
}

static double chop(artist* a,int range=5) {
 double sum=0.0;
 double* buffer = a->buffer;
 int step=range/2;
 if(step==0) step=1;
 double count = ((SX-range) / step)*((SY-range)/step);

 for(int i=0;i<SX-range;i+=step) 
  for(int j=0;j<SY-range;j+=step)
   sum+=std_block(buffer,i,j,range); 
 return sum/count;
}

static double compression(artist*a) {
 char dest[SX*SY*2];
 char src[SX*SY];
 unsigned char *src_ptr=(unsigned char*)src;
 double *buf_ptr=a->buffer;
 unsigned int destLen = sizeof(dest);
 unsigned int srcLen = sizeof(src);
 for(int i=0;i<SX*SY;i++)
 {
  src_ptr[i]=(unsigned char)(buf_ptr[i]*255.0);
 }

 BZ2_bzBuffToBuffCompress(dest,&destLen,src,srcLen,9,0,30);
 double comp=(((double)srcLen-(double)destLen)/(double)srcLen);
 return comp;
}
static double symmetry_x(artist* a) {
double sum=0.0;
double* buffer = a->buffer;
for(int x=0;x<SX;x++)
 for(int y=0;y<SY/2;y++)
  {
  double delta=buffer[y*SX+x]-buffer[(SY-y-1)*SX+x];
  delta*=delta;
  sum+=delta; //absd(buffer[y*SX+x]-buffer[(SY-y)*SX+x]);
  }
return 1.0-(sum/(SX*SY/2));
}

static double symmetry_y(artist* a) {
double sum=0.0;
double* buffer = a->buffer;
for(int x=0;x<SX/2;x++)
 for(int y=0;y<SY;y++)
  {
  double delta=buffer[y*SX+x]-buffer[y*SX+(SX-x-1)];
  delta*=delta;
  sum+=delta; //absd(buffer[y*SX+x]-buffer[y*SX+(SX-x)]);
  }
return 1.0-(sum/(SX*SY/2));
}


static double wavelet(artist*a) { 
   int i, n = SX*SY;
      double *data = (double*)malloc (n * sizeof (double));
       double *abscoeff = (double*)malloc (n * sizeof (double));
       size_t *p = (size_t*)malloc (n * sizeof (size_t));
       
       memcpy(data,a->buffer,sizeof(double)*SX*SY);

       gsl_wavelet *w;
       gsl_wavelet_workspace *work;
     
       w = gsl_wavelet_alloc (gsl_wavelet_daubechies, 4);
       work = gsl_wavelet_workspace_alloc (n);
     
       gsl_wavelet2d_transform_forward (w, data, SX, SX,SY, work);
     
       for (i = 0; i < n; i++)
         {
           abscoeff[i] = fabs (data[i]);
         }
       
       gsl_sort_index (p, abscoeff, 1, n);

       double total=0.0;
       
       for (i = 0; i< n; i++) {
        total+=abscoeff[p[i]];
       }

       double target=0.95*total;

       double accum=0.0;
       for(i=n-1; i>=0; i--)
       {
	accum+=abscoeff[p[i]];
        if(accum>target)
         break;
       }       

	double compression= ((double)i) / ((double)n);
       //gsl_wavelet2d_transform_inverse (w, data, SX, SX,SY, work);
       
       gsl_wavelet_free (w);
       gsl_wavelet_workspace_free (work);
       free (data);
       free (abscoeff);
       free (p);
    return compression;
}

};

#endif 

