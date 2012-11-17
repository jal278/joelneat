%newobject *::copy;
%module hyperneat
%{
#include "evolve.h"
%}

void initialize();

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

static double maze_path_length(artist*a);
static double gmaze_path_length(artist*a);
static double maze_path_nodes(artist*a);
static double gmaze_path_nodes(artist*a);
};

class artist {
 public:
  double distance(artist*a);
  bool get_nanflag();
  bool get_valid();

  bool isvalid();

  void clear();
  void clear_all(); 
  void save(const char*fn);
  void load_new(const char*fn);
  const char* save_xml();
  double* render_opt(int index);
  static artist* load(const char*fn);
  static artist* load_xml(const char*txt);
  int complexity();
  static void random_seed();
  static void seed(int sd);
  artist();
  ~artist();
  artist* copy();
  double* render_all();
  double* render_picture();
  void map();
  bool isrendered();
  void mutate();
  void change();
  void make_random();
  double* render_big();
  PyObject* get_big();
  PyObject* get_picture();
  PyObject *get_picture_num(int i);
 
 int get_maze_path_length() { return maze_path_length; }
 int get_maze_nodes() { return maze_ndoes; }
};

class evaluator {
 public:
 PyObject* get_weights(); 
 double distance(evaluator*a);
 int complexity();
 void save(const char*fn);
 static evaluator* load(const char*fn);
 evaluator* copy();
 evaluator();
 ~evaluator();
 double evaluate_all(artist* a);
 double evaluate_artist(artist* a);
 void mutate();
};
