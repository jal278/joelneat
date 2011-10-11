#include <cstdlib>
#include <vector>
#include <math.h>
#include <iostream>
#define LUT_SIZE 2048
#define PI 3.1415926535
using namespace std;

double sin_lut[LUT_SIZE];
double gauss_lut[LUT_SIZE];

double absd(double d)
{
    if (d<0.0)
        return -d;
    return d;
}

double randfloat()
{
	return (double)(rand()%RAND_MAX)/RAND_MAX;
}

double randuniform(float min, float max)
{
	return randfloat()*(max-min)+min;
}

int randint(int min,int max)
{
	int range = max-min;
	return (rand()%range)+min;
}

bool chance(double prob)
{
	if (randfloat()<prob)
		return true;
	return false;
}

double sum(double* x,int cnt)
{
	double s=0.0;
	for (int k=0;k<cnt;k++)
		s+=x[k];
	return s;
}
double sigmoid_af(double* x,int cnt)
{
	double s=sum(x,cnt);
	return 2.0/(1.0+exp(-s))-1.0;
}

double sigmoid(double s)
{
	return 1.0/(1.0+exp(-s));
}

double abs_af(double* x,int cnt)
{
	double s=sum(x,cnt);
    if (s<0.0)
        return -s;
    return s;
}

double gaussian_af(double* x,int cnt)
{
    double s=sum(x,cnt);
    return exp(-(s*s));
}

double mod_af(double* x,int cnt)
{
    double s=sum(x,cnt);
    return s - (int)s;
}

double sin_af(double* x,int cnt)
{
    double s=sum(x,cnt);
    return sin(s*2.5);	
}

double linear_af(double* x,int cnt)
{
	return sum(x,cnt);
}

void generate_luts() {
double x[2]={0.0,0.0};
for(int i=0;i<LUT_SIZE;i++) {
 double sin_ind = ((double)i/(double)LUT_SIZE)*2.0*PI;
 x[0]=sin_ind;
 sin_lut[i]=sin_af(x,2);
 double gauss_ind = ((double)i/(double)LUT_SIZE)*8.0-4.0;
 x[0]=gauss_ind;
 gauss_lut[i]=gaussian_af(x,2);
}

}

//range x=0 to two-pi
double sin_af_approx(double* x,int cnt) {
double s=sum(x,cnt);
s=fmod(s,PI*2.0);
if(s<0.0) s+=PI*2.0;
int index = LUT_SIZE*(s/(PI*2));
return sin_lut[index];
}

//range x=-4 to x=4, outside range =0
double gaussian_af_approx(double*x,int cnt) {
double s=sum(x,cnt);
if(s>4.0 || s<-4.0) return 0.0;
int index= LUT_SIZE*((s+4.0)/8.0);
return gauss_lut[index];
}

double sigmoid_approx(double s) {
if(s>4.0) return 1.0;
double tmp= 1.0-0.25*s;
tmp*=tmp;
tmp*=tmp;
tmp*=tmp;
tmp*=tmp;
return 1.0/(1.0+tmp);
}

double sigmoid_af_approx(double* x,int cnt) {
	double s=sum(x,cnt);
	return 2.0*sigmoid_approx(s)-1.0; 
}

void test_shit() {
 double x[2]= {-4.0,0.0};
 double step=0.01;
 while(x[0]<4.0) {
 cout << x[0] << " " << gaussian_af_approx(x,2) << endl;
 x[0]+=step;
 }
}
