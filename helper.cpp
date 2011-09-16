#include <cstdlib>
#include <vector>
#include <math.h>
using namespace std;

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
	if(s<0.0) return (-s);
	else return s;
}

double gaussian_af(double* x,int cnt)
{
    double s=sum(x,cnt);
    return exp(-s);
}

double mod_af(double* x,int cnt)
{
    double s=sum(x,cnt);
    return s - (int)s;
}

double sin_af(double* x,int cnt)
{
    double s=sum(x,cnt);
    return sin(s);	
}

double linear_af(double* x,int cnt)
{
	return sum(x,cnt);
}
