#ifndef GA123
#define GA123
#include <vector>
#include <iostream>
#include <algorithm>
#include "helpers.h"
#include "tinyxml/tinyxml.h"
#include "datarec.h"

using namespace std;


class Singleton
{   public:
	float COMPAT_THRESH;
	int TARGET_SPECIES;

        static Singleton* GetInstance();
		static long int next_inno()
		{
			return GetInstance()->innovation++;
		}
		static int random_af()
		{
			return randint(0,GetInstance()->af.size());
		}
        long int innovation;
		vector<activation_function> af;
 
    private:
        Singleton()  { 
			COMPAT_THRESH=2.0;
			TARGET_SPECIES=8;
			innovation=200;
                        generate_luts();
			//test_shit();
			af.push_back(sigmoid_af_approx);
		
		//COMMENT OUT WHEN DOING ANN-evolvution
			af.push_back(abs_af);
			af.push_back(gaussian_af_approx);
			af.push_back(sin_af_approx);
		        af.push_back(linear_af);
		//WHEN DOING ANN-evolution
                	
			        //af.push_back(mod_af);
			cout << "In Ctor" << endl; }
        ~Singleton() { cout << "In Dtor" << endl; }


        // Not defined, to prevent copying
        Singleton(const Singleton& );
        Singleton& operator =(const Singleton& other);
};
 
class species;
class individual;
class population;
class evolve;

bool cmp(const individual *a, const individual *b);
bool cmp_adj(const individual *a, const individual *b);
bool cmp_beh(const individual *a, const individual *b);

class species
{
public:
	species(individual* i);
	vector<individual*> members;
	individual* prototype;
	void adjust_fitness();
	~species();
};

class noveltyitem;
class noveltyarchive;

class individual
{
public:
	individual();
	virtual ~individual();
	virtual individual* make_copy()=0;
	virtual TiXmlElement* create_xml() { return NULL; }
	virtual individual* load_xml(TiXmlElement* elem) { return NULL; }
	virtual double distance(individual* other)=0;
	virtual void mutate()=0;
	noveltyitem* noveltypoint;
	double behavior;
	double fitness;
	double adj_fitness;
	bool viable;
	species* spec;
};

class population
{
public:
	population(bool spec=false)
	{
		speciate=spec;
		dirty=true;
		compat_thresh=Singleton::GetInstance()->COMPAT_THRESH;
		target_species=Singleton::GetInstance()->TARGET_SPECIES;
	}
	~population()
	{
	for(int x=0;x<species_list.size();x++)
		delete species_list[x];
	}
	void load(individual* ind,const char* name)
	{
		TiXmlDocument doc(name);
		if (!doc.LoadFile()) return;
		TiXmlElement* pop=doc.FirstChildElement("population");

		TiXmlElement* elem=pop->FirstChildElement("CPPN"); //was Network,fix this
		for(elem;elem;elem=elem->NextSiblingElement())
		{
			individual* newind = ind->load_xml(elem);
			members.push_back(newind);
		}


	}
	
	void save(const char* name)
	{
			sort_reg();
			TiXmlElement* stuff=create_xml();
			TiXmlDocument doc(name);
			TiXmlDeclaration* decl = new TiXmlDeclaration( "1.0", "", "" );
			doc.LinkEndChild(decl);
			doc.LinkEndChild(stuff);
			doc.SaveFile();
    	}
    		
	TiXmlElement* create_xml()
	{
    TiXmlElement* net_node = new TiXmlElement("population");
	//cout << "popsize " << members.size() << endl;
	for(int i=0;i<members.size();i++)
	{
	//	cout << "member " << i << endl;
	//	cout << members[i] << endl;
	//	cout << members[i]->fitness << endl;
		net_node->LinkEndChild(members[i]->create_xml());
	}

	return net_node;
    }

	int target_species;
	double compat_thresh;
	vector<species*> species_list;
	vector<individual*> members;
	double max_fitness;
	double avg_fitness;
	bool dirty;
	bool speciate;
	
	void speciate_ind(individual* x)
	{
			bool found=false;
			for(int y=0;y<species_list.size();y++)
			{
				if (x->distance(species_list[y]->prototype)<compat_thresh)
				{
					x->spec=species_list[y];
					species_list[y]->members.push_back(x);
					found=true;
					break;
				}
			}
			if (!found)
			{
				species* new_spec= new species(x);
				x->spec=new_spec;
				species_list.push_back(new_spec);
			}
	}
	void speciate_pop()
	{
		
		//clean out all old species
		for(int x=0;x<species_list.size();x++)
			species_list[x]->members.clear();

		//speciate
		for(int x=0;x<members.size();x++)
		{
			speciate_ind(members[x]);
		}

		//clean up empty species
		    vector<species*>::iterator k;

			bool dirt=true;
			while(dirt)
			{
				dirt=false;
				for(k=species_list.begin();k!=species_list.end();k++)
				{
					if ((*k)->members.size()==0)
					{
                        species* to_del = (*k);
						species_list.erase(k);
						delete to_del;
						dirt=true;
						break;
					}
				}
			}		
	}

	void adjust_fitness()
	{
		for(int x=0;x<species_list.size();x++)
		{
		species_list[x]->adjust_fitness();	
		}
	}
	void sort_adj()
	{
		sort(members.begin(),members.end(),cmp_adj);
		reverse(members.begin(),members.end());
	}
	void sort_reg()
	{
		sort(members.begin(),members.end(),cmp);
		reverse(members.begin(),members.end());
	}
	void sort_behavior()
	{
		sort(members.begin(),members.end(),cmp_beh);
		reverse(members.begin(),members.end());
	}	

	void sortall()
	{
		if(speciate)
		{
		adjust_fitness();
		sort_adj();
		}
		else
		{
		sort_reg();
		}
		dirty=false;
	}

	void remove_worst()
	{
		if(dirty) sortall();
		individual* to_remove=members[members.size()-1];
		
		if(speciate)
		{
		species* spec=to_remove->spec;

		vector<individual*>::iterator it; 
		bool found=false;
        for(it=spec->members.begin();it!=spec->members.end();it++)
		{
                if ((*it)==to_remove)
                {
                    spec->members.erase(it);
                    found=true;
                    break;
                }
        }
        
        }
    
		members.pop_back();
		delete to_remove;
	}

	individual* reproduce_one()
	{
		int cutoff=(int)(0.6*members.size());
		individual* selected = members[randint(0,cutoff+1)];
		return reproduce(selected);
	}
	
	individual* reproduce(individual* selected)
	{
		individual* newind = selected->make_copy();
		newind->mutate();
		members.push_back(newind);

		dirty=true;

		if(speciate)
			speciate_ind(newind);

		return newind;

	}	

	individual* reproduce_fuss()
	{
		double bmin= (10000);
		double bmax= (-10000);
		for(int x=0;x<members.size();x++)
		{
			double nb = members[x]->behavior;
			if (nb < bmin)
				bmin=nb;

			if (nb > bmax)
				bmax=nb;
		}
		double tochoose=randuniform(bmin,bmax);
		double mindist=100000.0;

		individual* chosen=NULL;
		for(int x=0;x<members.size();x++)
		{
			double dist=absd(members[x]->behavior-tochoose);
			if (dist<mindist)
			{
				mindist=dist;
				chosen=members[x];
			}
		}
		return reproduce(chosen);
	}

	void calc_stats()
	{
		double mx_fit=0.0;
		double fit_sum=0.0;
		for(int x=0;x<members.size();x++)
		{
			double fitness = members[x]->fitness;
			fit_sum+=fitness;
			if (fitness>mx_fit)
				mx_fit=fitness;
		}
		max_fitness=mx_fit;
		avg_fitness=fit_sum/members.size();
	}

};

class domain
{
public:
	virtual void evaluate(individual* ind,data_record* r=NULL)=0;
};

class evolve
{
public:
	population* p;
	domain* d;
	double avg_fit;
	double max_fit;
	bool fuss;
	bool novelty;
	noveltyarchive* archive;
	data_rec record;
	int epoch_count;

	void evaluate_all()
	{
		for(int x=0;x<p->members.size();x++)
			d->evaluate(p->members[x]);
		
	}

	~evolve();

	evolve(population* pop,domain* dom,bool f=false,bool n=false);

	void print_status()
	{
		cout << "Epoch " << epoch_count << endl;
	        p->calc_stats();
		cout << "Avg fit " << p->avg_fitness << endl;
		cout << "Max fit " << p->max_fitness << endl; 
		cout << "Num species " << p->species_list.size() << endl;
	}
	
	void epoch(int len);
};

class simpleind:public individual
{
public:
	double val;
	simpleind()
	{
		val=0.0;
	}
	virtual individual* make_copy()
	{
		simpleind* k= new simpleind();
		k->val=val;
		return k;
	}
	virtual void mutate()
	{
		val+=randfloat()-0.5;
		if(val<0.0) val=0.0;
		if(val>100.0) val=100.0;
	}
	virtual double distance(individual* other) 
	{
		double d = ((simpleind*)other)->val-val;
		if (d<0) return -d;
		return d;
	}
};

class simpledom:public domain
{
public:
	virtual void evaluate(individual* ind,data_record* dr=NULL)
	{
		simpleind* k=(simpleind*)ind;
		k->fitness=k->val;
	}
};
#include "noveltyset.h"
#endif

