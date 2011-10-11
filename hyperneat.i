%newobject *::copy;
%module hyperneat
%{
#include "evolve.h"
%}

class feature_detector {
public:
static double average(artist* a); 
static double std(artist* a);
static double skew(artist* a);
static double kurtosis(artist* a);
static double chop(artist*a,int r=1);
static double compression(artist*a);
static double wavelet(artist*a);
static double symmetry_x(artist*a);
static double symmetry_y(artist*a);
};

class artist {
 public:
  bool get_nanflag();
  void clear_picture();
  void save(const char*fn);
  void load(const char*fn);
  const char* save_xml();
  void load_xml(const char*txt);
  int complexity();
  void random_seed();
  artist();
  ~artist();
  artist* copy();
  double* render_picture();
  bool isrendered();
  void mutate();
  double* render_big();
  PyObject* get_big();
  PyObject* get_picture();
};

class evaluator {
 public:
 int complexity();
 void save(const char*fn);
 void load(const char*fn);
 evaluator* copy();
 evaluator();
 ~evaluator();
 double evaluate_artist(artist* a);
 void mutate();
};
