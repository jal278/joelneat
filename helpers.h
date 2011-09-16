#ifndef HELPRS123
#define HELPRS123
#include <vector>
using namespace std;


typedef double(*activation_function)(double* x,int cnt);
double inline absd(double d);
double inline randfloat();
double inline randuniform(float min, float max);
int inline randint(int min,int max);
bool inline chance(double prob);
double inline sum(double* x,int cnt);
double inline sigmoid(double s);
double inline abs_af(double* x,int cnt);
double inline gaussian_af(double* x,int cnt);
double inline mod_af(double* x,int cnt);
double inline sigmoid_af(double* x,int cnt);
double inline linear_af(double* x,int cnt);
double inline sin_af(double* x,int cnt);
#endif

