#include "noveltyset.h"

//for sorting by novelty
bool cmp(const noveltyitem *a, const noveltyitem* b)
{
return a->novelty < b->novelty;
}

//for sorting by fitness
bool cmp_fit(const noveltyitem *a, const noveltyitem *b)
{
return a->fitness < b->fitness;
}

noveltyitem::noveltyitem(const noveltyitem& item)
{
	added=item.added;
	ind = item.ind->make_copy();
	//genotype=new Genome(*(item.genotype));
	// vphenotype=new Network(*(item.phenotype));
	age=item.age;
	fitness=item.fitness;
	novelty=item.novelty;
	generation=item.generation;
	indiv_number=item.indiv_number;
	for(int i=0;i<(int)item.data.size();i++)
	{
		vector<float> temp;
		for(int j=0;j<(int)item.data[i].size();j++)
			temp.push_back(item.data[i][j]);
		data.push_back(temp);		
	}
}

//evaluate the novelty of the whole population
void noveltyarchive::evaluate_population(population* pop,bool fitness)
{
	population *p = (population*)pop;
	vector<individual*>::iterator it;
	for(it=p->members.begin();it<p->members.end();it++)
		evaluate_individual((*it),pop,fitness);
}

//evaluate the novelty of a single individual
void noveltyarchive::evaluate_individual(individual* ind,population* pop,bool fitness)
{
	float result;
	if(fitness)  //assign fitness according to average novelty
	{
		result = novelty_avg_nn(ind->noveltypoint,-1,false,pop);
		ind->fitness = result;
	} 
	else  //consider adding a point to archive based on dist to nearest neighbor
	{
		result = novelty_avg_nn(ind->noveltypoint,1,false);
		ind->noveltypoint->novelty=result;
		if(add_to_novelty_archive(result))
				add_novel_item(ind->noveltypoint);
	}
}
