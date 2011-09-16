#include <vector>
#include "ga.h"

using namespace std;
bool cmp(const individual *a, const individual *b)
{
return a->fitness < b->fitness;
}


bool cmp_adj(const individual *a, const individual *b)			
{
return a->adj_fitness < b->adj_fitness;
}

bool cmp_beh(const individual *a, const individual *b)
{
return a->behavior < b->behavior;
}


float metric(noveltyitem* a,noveltyitem* b)
{
	float d=0.0;
	//cout << a->data[0].size() << " " << b->data[0].size() << endl;

	if( a->data.size() != b->data.size())
		cout << "BLAHHHHH" << a->data.size() << " " << b->data.size() <<endl;
	
	if (a->data[0].size() != b->data[0].size())
		cout << "Size incompatability!" << a->data[0].size() << " " << b->data[0].size() << " " <<endl;

	for(int x=0;x<a->data[0].size();x++)
	{
		float delta=a->data[0][x]-b->data[0][x];
		delta*=delta;
		d+=delta;
	}
	return d;
}

individual::individual()
{
noveltypoint=NULL;
viable=true;
}

individual::~individual()
{
if(noveltypoint && !noveltypoint->added)
	delete noveltypoint;
}

void species::adjust_fitness()
	{
			int spec_size=members.size();
			for(int y=0;y<spec_size;y++)
			{
		                individual* to_adj = members[y];
				to_adj->adj_fitness=to_adj->fitness/spec_size;
			}
	}


evolve::~evolve()
{
if(archive!=NULL)
			delete archive;
}

void evolve::epoch(int len)
{
		epoch_count++;

		print_status();
		for(int x=0;x<len;x++)
		{
			if(x%15==0 && p->speciate)
			{
				if(novelty) {
				   //update fittest individual list		
	   			   archive->update_fittest(p);
				   //refresh generation's novelty scores
				   archive->evaluate_population(p,true);
				   
				}

				p->speciate_pop();
				if (p->species_list.size()>p->target_species)
					p->compat_thresh*=1.1;
				else if (p->species_list.size()<p->target_species)
					p->compat_thresh*=0.9;	
			}
	
			individual* k;
			if(!fuss)	
				k=p->reproduce_one();
			else
				k=p->reproduce_fuss();
			
			data_record* dr = new data_record();
			d->evaluate(k,dr);
			archive->update_fittest(k);
			record.add_new(dr);
			
			if(novelty)
			{
				archive->evaluate_individual(k,p);
				if(!k->viable)
					k->fitness/=20.0;			
			}
			k->spec->adjust_fitness();
			p->remove_worst();
			
			
	}

	if(novelty) {
			archive->end_of_gen_steady(p);
		
			archive->evaluate_population(p,false);
			cout << "ARCHIVE SIZE:" << 
			archive->get_set_size() << endl;
			cout << "ARCHIVE THRESHOLD:" <<
			archive->get_threshold() << endl;
	}
}

evolve::evolve(population* pop,domain* dom,bool f,bool n)
{
		epoch_count=0;
		fuss=f;
		avg_fit=0.0;
		max_fit=0.0;
		p=pop;
		d=dom;
		novelty=n;

		archive = new noveltyarchive(10.0,metric,true);

		evaluate_all();

		if(novelty) {
		  //assign fitness scores based on novelty
		  archive->evaluate_population(p,true);
		  //add to archive
  		archive->evaluate_population(p,false);
		}

		if(p->speciate)
			p->speciate_pop();

		
}

