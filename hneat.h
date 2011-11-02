#ifndef HNEAT
#define HNEAT

#include <vector>
#include <algorithm>
#include <math.h>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include "tinyxml/tinyxml.h"
#include "helpers.h"
#include "ga.h"

using namespace std;

class Substrate;
class CPPN;
class Node;
class Connection;

void test_evolve_xor();

class Network:public individual
{
public:
	bool created;
	Network(vector<Substrate*>& subs,vector<CPPN*>& cppn);
	virtual TiXmlElement* create_xml();
	Network() { noveltypoint=NULL; }
	Network* Copy();
	void fix_weights();
	void mutate_add_substrate();
	void mutate_add_CPPN();
	void change();
	virtual void mutate(); 
	virtual double distance(individual* other);
	virtual individual* make_copy(); 
	void create();
        int complexity();
	virtual individual* load_xml(TiXmlElement* elem)
	{
		return (individual*)Network::load(elem);
	}

	static Network* load(const char* fn)
	{
		TiXmlDocument doc(fn);
		if (!doc.LoadFile()) return NULL;
		Network* newnet = Network::load(doc.FirstChildElement("network"));
		return newnet;
	}

	void save(const char* name)
	{
			TiXmlElement* stuff=create_xml();
			TiXmlDocument doc(name);
			TiXmlDeclaration* decl = new TiXmlDeclaration( "1.0", "", "" );  
			doc.LinkEndChild(decl);
			doc.LinkEndChild(stuff);
			doc.SaveFile();
	}
	static Network* load(TiXmlElement* net_xml);
    	virtual ~Network();
   
	void activate();
        void flush();
	vector<Substrate*> substrates;
	vector<Substrate*> inputs;
	vector<Substrate*> outputs;
	vector<CPPN*> cppns;
	
};

class Substrate
{
public:
	bool trivial;

	//used for trivial node
	double sum;
	double activation;
	
	
	vector<int> resolutions;

	int dim;
	long int innovation;
	long int num_neurons;
	
	double *sum_matrix;
        double *bias_matrix;
	double *activation_matrix;

	bool input;
	bool output;
	bool bias;
	
	bool zerobased; //whether coordinates are based on [0..1] or [-1..1]

	vector<CPPN*> in_conn;
	vector<CPPN*> out_conn;
	
   void load_in(double *input)
   {
        for(int x=0;x<num_neurons;x++) {
            activation_matrix[x]=input[x];
        }
    }
    
    vector<int> max_activation()
    {
        double max = (-1000.0);
        
        int the_max=0;
        
        vector<int> coord;
        
        for(int x=0;x<dim;x++)
            coord.push_back(0);
            
        for(int x=0;x<num_neurons;x++)
        {
            //cout << activation_matrix[x] << " ";
            if (activation_matrix[x]>max)
            {
                the_max=x;
                max=activation_matrix[x];
            }
        }
        //cout << endl;
        
        int remainder=the_max;
        for(int x=resolutions.size()-1;x>=0;x--)
        {
            int next=(remainder/multiplier[x]);    
            coord.push_back(next);
            remainder-=(next*multiplier[x]);
        }
        
        
        reverse(coord.begin(),coord.end());
        
        return coord;
    }

	vector<long int> multiplier;
	void flush()
	{
		//reset trivial components
		sum=0.0;
		activation=0.0;
		//reset rest of components
		for(int x=0;x<num_neurons;x++)
		{
			sum_matrix[x]=0.0;
			activation_matrix[x]=0.0;
		}
	}


	static Substrate* load(TiXmlElement* sub_xml)
	{
		bool zero = (bool)atoi(sub_xml->Attribute("zerobased"));
		bool input = (bool)atoi(sub_xml->Attribute("input"));
		bool output = (bool)atoi(sub_xml->Attribute("output"));
		bool bias = (bool)atoi(sub_xml->Attribute("bias"));
		long int innovation = atol(sub_xml->Attribute("innovation"));

		vector<int> res;
		TiXmlElement* res_node=sub_xml->FirstChildElement("resolutions");

		TiXmlElement* elem=res_node->FirstChildElement("resolution");
		for(elem;elem;elem=elem->NextSiblingElement())
		{
			int r;
			elem->Attribute("resolution",&r);
			res.push_back(r);
		}
		Substrate* k = new Substrate(res,input,output,bias,innovation);
		k->zerobased=zero;
		return k;
	}

	TiXmlElement* create_xml()
	{
		char outstring[100];
		
		TiXmlElement* sub_node= new TiXmlElement("substrate");
		
		sprintf(outstring,"%d",zerobased);
		sub_node->SetAttribute("zerobased",outstring);	

		sprintf(outstring,"%d",input);
		sub_node->SetAttribute("input",outstring);

		sprintf(outstring,"%d",output);
		sub_node->SetAttribute("output",outstring);

		sprintf(outstring,"%d",bias);
		sub_node->SetAttribute("bias",outstring);

		sprintf(outstring,"%ld",innovation);
		sub_node->SetAttribute("innovation",outstring);


		TiXmlElement* res_node= new TiXmlElement("resolutions");
		for(int x=0;x<resolutions.size();x++)
		{
			TiXmlElement* newres = new TiXmlElement("resolution");
			newres->SetAttribute("resolution",resolutions[x]);
			res_node->LinkEndChild(newres);
		}
		sub_node->LinkEndChild(res_node);
		return sub_node;
	}

	Substrate* Copy()
	{
		Substrate* k = new Substrate(resolutions,input,output,bias,innovation);
		k->zerobased = zerobased;
		return k;
	}

	Substrate(vector<int> res,bool inp,bool out,bool biasp,long int inno)
	{
		zerobased=false;
		innovation=inno;

		bias=biasp;
		input=inp;
		output=out;

		back_insert_iterator<vector<int> > citer (resolutions);
		copy(res.begin(),res.end(),citer);

		long int mult=1;
		dim=res.size();
		//trivial substrate is a single neuron
		if(dim==0)
		{
			trivial=true;
		}
		else
		{
			trivial=false;
		}

		for(int x=0;x<dim;x++)
		{
			multiplier.push_back(mult);
			mult*=res[x];
		}
		num_neurons=mult;

		sum_matrix=(double*)malloc(sizeof(double)*num_neurons);
                bias_matrix=(double*)malloc(sizeof(double)*num_neurons);
                for(int x=0;x<num_neurons;x++)
                 bias_matrix[x]=0.0;
		activation_matrix=(double*)malloc(sizeof(double)*num_neurons);
	}
	~Substrate()
	{
 		free(sum_matrix);
 	        free(bias_matrix);
                free(activation_matrix);
	}
	void update();

};

class Connection
{

public:
	Connection(Node* in_node,Node* out_node,double weight, long int inn);
	
	static Connection* load(TiXmlElement* node_xml,vector<Node*> nodes);

	Connection* Copy(vector<Node*> nlist);


	void mutate(bool cold=false)
	{
		if (cold)
		{
			weight=randfloat()*6.0-3.0;
		}
		else
		{
			weight+=randfloat()*1.0-0.5;
			if(weight>3.0)
				weight=3.0;
			else if (weight<(-3.0))
				weight=(-3.0);
		}
	}

   TiXmlElement* create_xml();

	int touch_flag;
	long int innovation;
	double weight;
	double value;
	Node* in_node;
	Node* out_node;
	void flush()
	{
		touch_flag=0;
	}
	void update();

	double get_value() { return value;	}
};

class Node
{
public:
	Node(bool input,bool output,bool bias,int af,long int inno):input(input),output(output),bias(bias),innovation(inno)
	{
		activation_fn=af;
		activation=Singleton::GetInstance()->af[af];
	}

	Node* Copy()
	{
		return new Node(input,output,bias,activation_fn,innovation);
	}

	static Node* load(TiXmlElement* node_xml)
	{
		bool input=(bool)atoi(node_xml->Attribute("input"));
		bool output=(bool)atoi(node_xml->Attribute("output"));
		bool bias=(bool)atoi(node_xml->Attribute("bias"));
		int innovation=atoi(node_xml->Attribute("innovation"));
		int af=atoi(node_xml->Attribute("activation_fn"));

		Node* k= new Node(input,output,bias,af,innovation);
		return k;
	}

	TiXmlElement* create_xml()
	{
		char outstring[100];
		
		TiXmlElement* node_xml= new TiXmlElement("node");
		
		sprintf(outstring,"%d",input);
		node_xml->SetAttribute("input",outstring);

		sprintf(outstring,"%d",output);
		node_xml->SetAttribute("output",outstring);

		sprintf(outstring,"%d",bias);
		node_xml->SetAttribute("bias",outstring);

		sprintf(outstring,"%d",innovation);
		node_xml->SetAttribute("innovation",outstring);

		sprintf(outstring,"%d",activation_fn);
		node_xml->SetAttribute("activation_fn",outstring);

		return node_xml;
	}

	bool input;
	bool output;
	bool bias;
        double node_bias;
	double node_output;
	double node_sum;
	int touch_flag;
	long int innovation;
	int activation_fn;
	activation_function activation;
	vector<Connection*> in_conn;
	vector<Connection*> out_conn;
	void set_output(double in) { node_output=in; }
	double get_output() { return node_output; }
	void flush()
	{
		touch_flag=0;
		if(!input)
			node_output=0.0;
		if(bias)
			node_output=1.0;
	}
	void update()
	{
		if(!input)
		{
		        double inps[100];
			int sz = in_conn.size();
			node_sum=node_bias;
                        inps[sz]=node_bias;
			for(int x=0;x<sz;x++)
			{
				in_conn[x]->update();
				inps[x]=in_conn[x]->get_value();
			}
			node_output=activation(inps,sz);			
		}
	}
};


class CPPN:public individual
{
public:
	bool created;
	bool trivial;
        double trivial_weight;

	Substrate* in_substrate;
	Substrate* out_substrate;
	long int innovation;
	int dim;
	int net_depth;
	vector<Node*> nodes;
	vector<Node*> inputs;
	vector<Node*> outputs;
	vector<Connection*> connections;
        int complexity();
	vector<int> inp_res;
	vector<int> out_res;
	vector<int> total_res;

	vector<long int> inp_mult;
	vector<long int> out_mult;
	vector<long int> total_mult;

	vector<double> inp_inc;
	vector<double> out_inc;
	vector<double> total_inc;

	double* weight_matrix;
        bool nanflag;
	void fix_weights();	
	void mutate_links()
	{
        for(int x=0;x<connections.size();x++)
            connections[x]->mutate(true);
  	  }
	
	virtual individual* make_copy()
	{
		vector<Substrate*> blah;
		blah.push_back(in_substrate);
		blah.push_back(out_substrate);
		CPPN* copy = Copy(blah);
	}
	CPPN* Copy(vector<Substrate*> subs)
	{
		Substrate* i=NULL;
		Substrate* o=NULL;
		
		if(in_substrate!=NULL)                 
		for(int x=0;x<subs.size();x++)
		{
			if (subs[x]->innovation==in_substrate->innovation)
				i=subs[x];
			if (subs[x]->innovation==out_substrate->innovation)
				o=subs[x];

		}
                
		vector<Node*> n;
		vector<Connection*> c;
		
		for(int x=0;x<nodes.size();x++)
			n.push_back(nodes[x]->Copy());
		for(int x=0;x<connections.size();x++)
			c.push_back(connections[x]->Copy(n));

		return new CPPN(i,o,innovation,n,c,trivial_weight);
	}
	virtual ~CPPN()
	{
		if(created)
			free(weight_matrix);
		for(int x=0;x<nodes.size();x++)
			delete nodes[x];
		for(int x=0;x<connections.size();x++)
			delete connections[x];
	}	
	virtual double distance(individual* ind)
	{
		CPPN* c2 = (CPPN*)ind;
		int excess=0;
		int disjoint=0;
		int matching=0;
		double weight_dif=0.0;

		CPPN* c1 = this;
		long int c1inno=0;
		long int c2inno=0;
		int c1index=0;
		int c2index=0;
		
		int c1size=c1->connections.size();
		int c2size=c2->connections.size();
		int c1max=c1->connections[c1size-1]->innovation;
		int c2max=c2->connections[c2size-1]->innovation;
		
		while(c1index<c1size && c2index<c2size)
		{
			c1inno=c1->connections[c1index]->innovation;
			c2inno=c2->connections[c2index]->innovation;
			//cout << "c1: " <<c1inno << " " << "c2: " <<c2inno <<endl;
			if(c1inno==c2inno)
			{
				matching++;
				double d=c1->connections[c1index]->weight-c2->connections[c2index]->weight;

		

				if (d<0)
					d=(-d);
				weight_dif+=d;
				c1index++;
				c2index++;
			}
			else if (c1inno<c2inno)
			{
				c1index++;
				disjoint++;
			}
			else
			{
				c2index++;
				disjoint++;
			}
		}
		
		int e1 = c2size-c2index;
		int e2 = c1size-c1index;
		excess = max(e1,e2);
		if (matching>0)
		{
			weight_dif/=matching;
		}
		// cout << "wd: " << weight_dif << " mtch:" << matching << " exc:" << excess << " dj:" << disjoint << endl;
		return weight_dif*3.0+excess*2.0+disjoint*1.0;
	}

	void mutate_add_link()
	{
		int num_tries=30;
		bool found=false;
		Node *n1,*n2;
		while(num_tries>0 && !found)
		{
			found=true;
			
			n1=nodes[randint(0,nodes.size())];
			n2=nodes[randint(0,nodes.size())];
			
			if (n2->input)
				found=false;

			if (n2->bias)
				found=false;

			if (n1==n2)
				found=false;
			
			for(int x=0;x<connections.size();x++)
				if (connections[x]->in_node==n1 &&
					connections[x]->out_node==n2)
						found=false;

			if (recurrent(n1,n2))
				found=false;
			num_tries--;
		}

		//unsuccessful
		if (!found)
			return;

		Connection* k = new Connection(n1,n2,0.0,Singleton::next_inno());
		k->mutate(true);
		
		//add the new connection
		connections.push_back(k);
	}
        void make_random() {
         int new_nodes = randint(0,6);
         int new_links = randint(0,10);
         for(int k=0;k<new_nodes;k++)       
		 mutate_add_node();
         for(int k=0;k<new_links;k++)
	 	mutate_add_link();
         change();
	}
	void change()
	{
		for(int x=0;x<connections.size();x++)
		{
			connections[x]->mutate(true);
		}
		mutate_trivial(true);
	}

	void mutate_add_node()
	{
		bool found=false;
		Connection* to_split;

		//don't want to split bias connections
		while(!found)
		{
		
		found=true;

		//choose random connection
		to_split = connections[randint(0,connections.size())];
		
		if (to_split->in_node->bias)
			found=false;
		}

		//create new node
		Node* newnode = new Node(false,false,false,Singleton::random_af(),Singleton::next_inno());
		Connection* c1 = new Connection(to_split->in_node,newnode,0.0,Singleton::next_inno());
		Connection* c2 = new Connection(newnode,to_split->out_node,0.0,Singleton::next_inno());
		
		c1->mutate(true);
		c2->mutate(true);

		//initially minimize impact of new connection
		c2->weight/=4.0;
		
		nodes.push_back(newnode);
		connections.push_back(c1);
		connections.push_back(c2);
	}
	
	void mutate_trivial(bool cold=false)
	{
        if(cold)
            trivial_weight=randfloat()*4.0-2.0;
        else
            {
                trivial_weight+=(randfloat()-0.5);
                if(trivial_weight>8.0)
                    trivial_weight=8.0;
                else if (trivial_weight<(-8.0))
                    trivial_weight=(-8.0);
            }
    }
	virtual void mutate()
	{
		if(!trivial)
		{
//FIXME: MUTATION IS CRAZY HIGH, SHOULD BE SEPARATE PARAMETERRRR
		//add_link mutation
		if (chance(0.1))
			 mutate_add_link();
		
		//add_node mutation
		if (chance(0.05))
			mutate_add_node();

	
		for(int x=0;x<connections.size();x++)
			if(chance(0.6))
				connections[x]->mutate();
		}	

		if (trivial)
		{
		    if(chance(0.4))
		    mutate_trivial();
        	}
	
	}
	void update()
	{
		int in_dim = in_substrate->dim;
		int out_dim = out_substrate->dim;

		if (dim==0)
		{
			out_substrate->sum+=(in_substrate->activation*trivial_weight);
		}
		else if(in_dim==0)
		{
			for(int x=0;x<out_substrate->num_neurons;x++)
			{
				out_substrate->sum_matrix[x]+=in_substrate->activation*weight_matrix[x];
			}
		}
		else if(out_dim==0)
		{
			for(int x=0;x<in_substrate->num_neurons;x++)
			{
                                //cout << in_substrate->activation_matrix[x] << " " << weight_matrix[x] << endl;
				out_substrate->sum+=in_substrate->activation_matrix[x]*weight_matrix[x];
				//	cout << out_substrate->sum << endl;
			}
		}
		else if (in_dim>0 && out_dim>0)
		{
			long int row = in_substrate->num_neurons;
			long int accum=0;
			int out_neurons = out_substrate->num_neurons;
			int in_neurons = in_substrate->num_neurons;
			double* out=out_substrate->sum_matrix;
			double* in=in_substrate->activation_matrix;
			
			for(int x=0;x<out_neurons;x++)
			{
				for(int y=0;y<in_neurons;y++)
				{
					out[x]+=weight_matrix[accum]*in[y];
					accum++;
				}
			}
		}
	}

	void generate_weight_matrix()
	{
		long int mul=1;
                inp_res.clear();
                out_res.clear();
                inp_mult.clear();
		out_mult.clear();
                inp_inc.clear();
		out_inc.clear();
                total_res.clear();
                total_inc.clear();
                total_mult.clear();

		inp_res.reserve(3);
		out_res.reserve(3);
		inp_mult.reserve(3);
		inp_inc.reserve(3);
		out_mult.reserve(3);
		out_inc.reserve(3);
		total_res.reserve(6);
		total_inc.reserve(6);
		total_mult.reserve(6);
		back_insert_iterator< vector<int> > in_iter(inp_res);
		back_insert_iterator< vector<int> > out_iter(out_res);

		//no weight matrix for trivial CPPN (single weight)
		if(trivial)
			return;
                if(created)
                 free(weight_matrix);
		created=true;
		
		copy(in_substrate->resolutions.begin(),in_substrate->resolutions.end(),in_iter);
		copy(out_substrate->resolutions.begin(),out_substrate->resolutions.end(),out_iter);
	
		double coordinate[100];
		int count[100];
		for(int x=0;x<inp_res.size();x++)
		{
			inp_mult.push_back(mul);
			count[x]=0;
			if(in_substrate->zerobased)
			{
				coordinate[x]=(0.0);
				inp_inc.push_back(1.0/(inp_res[x]-1));
			}
			else
			{			
				coordinate[x]=(-1.0);			
				inp_inc.push_back(2.0/(inp_res[x]-1));
			}
			mul*=inp_res[x];
		}
		
		int isize=inp_res.size();

		for(int x=0;x<out_res.size();x++)
		{
			out_mult.push_back(mul);

			count[x+isize]=0;
			if(in_substrate->zerobased)
			{
				out_inc.push_back(1.0/(out_res[x]-1));
				coordinate[x+isize]=(0.0);			
			}
			else
			{
				out_inc.push_back(2.0/(out_res[x]-1));
				coordinate[x+isize]=(-1.0);			
			}
			mul*=out_res[x];
		}

		total_res.insert(total_res.end(),inp_res.begin(),inp_res.end());
		total_res.insert(total_res.end(),out_res.begin(),out_res.end());
		total_mult.insert(total_mult.end(),inp_mult.begin(),inp_mult.end());
		total_mult.insert(total_mult.end(),out_mult.begin(),out_mult.end());
		total_inc.insert(total_inc.end(),inp_inc.begin(),inp_inc.end());
		total_inc.insert(total_inc.end(),out_inc.begin(),out_inc.end());
		//fill in weight matrix
		weight_matrix=(double*)malloc(sizeof(double)*mul);

                //for normalizing weights
                double pos_weight_sum=0.0;
                double neg_weight_sum=0.0;
                int output_begin=0;
                int output_end=0;
		for(int x=0;x<mul;x++)
		{
            /*
            if (x%10000==0)
            {
                cout << x << endl;
            }
            */
			bool b=false;
			
			
			double the_weight=query_net(coordinate); //query with current coordinates
            		
            //suppress weight
            double cutoff=0.2;
            if(absd(the_weight)<cutoff)
            {
                the_weight=0.0;
            }
            else
            {
                if(the_weight<0.0)
                    the_weight+=cutoff;
                else
                    the_weight-=cutoff;
                //rescale weight          
                the_weight*=(1.0/(1.0-cutoff))*3.0;
            }
           

            weight_matrix[x]=the_weight;
            if(the_weight>=0)
             pos_weight_sum+=the_weight;
            else
             neg_weight_sum-=the_weight;
             
	    int k=0;
			//now find proper way to increment coordinate
			//increment least significant dimension first
			if((x+1)!=mul)
			do {
				count[k]++;
				coordinate[k]+=total_inc[k];
				if(count[k]==total_res[k])
				{
					b=true;
					count[k]=0;
					coordinate[k]=(-1);
					k++;
				}
				else
				{
					b=false;
				}
			} while(b);
                        
                     
                        //if we are changing dest ndoe
			if(k>=isize || (x+1)==mul) {
                         if((x+1)==mul) 
                          output_end=x+1;
                         else output_end=x;
                         for(int wptr=output_begin;wptr<output_end;wptr++) {
                          if(weight_matrix[wptr]>0.0 && pos_weight_sum>0.0)
                             weight_matrix[wptr]/=(pos_weight_sum/3.0);
	 		  else if(weight_matrix[wptr]<0.0 && neg_weight_sum>0.0) 
                             weight_matrix[wptr]/=(neg_weight_sum/3.0); 
                          }
                          //reset weight normalization conuters
                          output_begin=output_end;
                          pos_weight_sum=0.0;
                          neg_weight_sum=0.0;
                        }
		}
	}

	TiXmlElement* create_xml();

	virtual individual* load_xml(TiXmlElement* elem)
	{
		return (individual*)CPPN::load(elem);
	}
        
        static CPPN* load_xml(const char *xml_string)
        {
		TiXmlDocument doc;
                doc.Parse(xml_string,0,TIXML_ENCODING_UTF8);
		CPPN* newcppn = CPPN::load(doc.FirstChildElement("CPPN"));
		//CPPN* newcppn = CPPN::load(doc.FirstChildElement("CPPN"),substrate_list);
		return newcppn;
	}
 
	static CPPN* load(const char* fn)
	{
		TiXmlDocument doc(fn);
		if (!doc.LoadFile()) return NULL;
		CPPN* newcppn = CPPN::load(doc.FirstChildElement("CPPN"));
		//CPPN* newcppn = CPPN::load(doc.FirstChildElement("CPPN"),substrate_list);
		return newcppn;
	}

	static CPPN* load(const char* fn,vector<Substrate*> substrate_list)
	{
		TiXmlDocument doc(fn);
		if (!doc.LoadFile()) return NULL;
		CPPN* newcppn = CPPN::load(doc.FirstChildElement("CPPN"),substrate_list);
		return newcppn;
	}

	double query_net(double* inputs,int out=0)
	{
		double k[10];
		flush();
		load_inputs(inputs);
		for(int x=0;x<(net_depth+1);x++)
			activate();
		get_outputs(k);
                if(isnan(k[out]))
        	{
	         nanflag=true;
		}
		return k[out];
	}

	static CPPN* load(TiXmlElement* node,vector<Substrate*>& substrates) 
	{
		Substrate *source=NULL, *target=NULL;
		bool trivial=atoi(node->Attribute("trivial"));
		double trivial_weight=atof(node->Attribute("trivial_weight"));
		int dim=atoi(node->Attribute("dimensionality"));
		int in_sub=atoi(node->Attribute("in_substrate"));
		int out_sub=atoi(node->Attribute("out_substrate"));
                cout << "in load." << endl;
                for(int i=0;i<substrates.size();i++) {
                 if(substrates[i]->innovation == in_sub) source=substrates[i];
                 if(substrates[i]->innovation == out_sub) target=substrates[i];      		}
                cout << in_sub << " " << out_sub << endl;
                if((in_sub==NULL) || (out_sub==NULL)) cout <<"null..." << endl;

		long int innovation=atol(node->Attribute("innovation"));

		TiXmlElement* nodes_xml = node->FirstChildElement("nodes");
		TiXmlElement* conn_xml = node->FirstChildElement("connections");

		TiXmlElement* elem = nodes_xml->FirstChildElement("node");
		vector<Node*> nodes;
		for(elem;elem;elem=elem->NextSiblingElement())
		{
			nodes.push_back(Node::load(elem));
		}
		
		elem=conn_xml->FirstChildElement("connection");
		vector<Connection*> connections;
		for(elem;elem;elem=elem->NextSiblingElement())
		{
			connections.push_back(Connection::load(elem,nodes));
		}
		CPPN* k = new CPPN(source,target,innovation,
							nodes,connections,trivial_weight);
		return k;
 }
	
        static CPPN* load(TiXmlElement* node)
	{
		bool trivial=atoi(node->Attribute("trivial"));
		double trivial_weight=atof(node->Attribute("trivial_weight"));
		int dim=atoi(node->Attribute("dimensionality"));
		//int in_sub=atoi(node->Attribute("in_substrate"));
		//int out_sub=atoi(node->Attribute("out_substrate"));
		long int innovation=atol(node->Attribute("innovation"));

		TiXmlElement* nodes_xml = node->FirstChildElement("nodes");
		TiXmlElement* conn_xml = node->FirstChildElement("connections");

		TiXmlElement* elem = nodes_xml->FirstChildElement("node");
		vector<Node*> nodes;
		for(elem;elem;elem=elem->NextSiblingElement())
		{
			nodes.push_back(Node::load(elem));
		}
		
		elem=conn_xml->FirstChildElement("connection");
		vector<Connection*> connections;
		for(elem;elem;elem=elem->NextSiblingElement())
		{
			connections.push_back(Connection::load(elem,nodes));
		}
 		
		CPPN* k = new CPPN(NULL,NULL,innovation,
							nodes,connections,trivial_weight);
		return k;
	}

        TiXmlPrinter printer;
        const char* save_xml() 
        {
	TiXmlElement* stuff=create_xml();
	TiXmlDocument doc;
	TiXmlDeclaration* decl = new TiXmlDeclaration( "1.0", "", "" );  
	doc.LinkEndChild(decl);
	doc.LinkEndChild(stuff);
        doc.Accept(&printer);
        return printer.CStr();
        }
	
	void save(const char* name)
	{
	TiXmlElement* stuff=create_xml();
	TiXmlDocument doc(name);
	TiXmlDeclaration* decl = new TiXmlDeclaration( "1.0", "", "" );  
	doc.LinkEndChild(decl);
	doc.LinkEndChild(stuff);
	doc.SaveFile();
	}

	CPPN(Substrate* source, Substrate* target,long int inno,bool minimize=false)
	{
		vector<Node*> n;
		vector<Connection*> c;

		int temp_inno = 0;

		n.reserve(10);
		c.reserve(10);

		//add inputs for each dimension of source & target substrate
		for(int x=0;x<source->dim;x++)
			n.push_back(new Node(true,false,false,0,temp_inno++));

		for(int x=0;x<target->dim;x++)
			n.push_back(new Node(true,false,false,0,temp_inno++));

		//add bias
		n.push_back(new Node(false,false,true,0,temp_inno++));
                int num_outputs=2;	
		//add output
		for(int x=0;x<num_outputs;x++)
		n.push_back(new Node(false,true,false,0,temp_inno++));

		//add connections
		int tot_dim=source->dim+target->dim;
		for(int x=0;x<(tot_dim+1);x++)
		{
			for(int y=0;y<num_outputs;y++) {
			c.push_back(new Connection(n[x],n[tot_dim+1+y],0.0,temp_inno++));
			c[x*num_outputs+y]->mutate(true);
			}	
		}

		if(minimize)
			c[tot_dim]->weight-=3.0;			

		init(source,target,inno,n,c,0.0);
	}
	void init(Substrate* source,Substrate* target,long int inno,vector<Node*>& n, vector<Connection*>& c,double trivweight)
	{
		nanflag=false;
		trivial_weight=trivweight;
		in_substrate=source;
		out_substrate=target;
		created=false;
		connections.reserve(10);
		nodes.reserve(10);		

		innovation=inno;
	
		back_insert_iterator<vector<Connection*> > destc (connections);
		back_insert_iterator<vector<Node*> > destn (nodes);
		copy(c.begin(),c.end(),destc);
		copy(n.begin(),n.end(),destn);

		for(int x=0;x<n.size();x++)
		{
			if (nodes[x]->input)
				inputs.push_back(nodes[x]);
			else if (nodes[x]->output)
				outputs.push_back(nodes[x]);
		}
        if(in_substrate!=NULL && out_substrate!=NULL) {		
        in_substrate->out_conn.push_back(this);
        out_substrate->in_conn.push_back(this);
        }
		dim=inputs.size(); //source->dim+target->dim;
		
		//trivial CPPN is equal to a connection
		if(dim==0)
			trivial=true;
		else
			trivial=false;
		
		net_depth = depth();
	
	}

	CPPN(Substrate* source,Substrate* target,long int inno,vector<Node*>& n, vector<Connection*>& c,double trivweight)
	{
		init(source,target,inno,n,c,trivweight);	
	}

	bool recurrent(Node* s, Node* t)
	{
		flush();
		if(is_path(t,s))
			return true;
		return false;
	}
	bool is_path(Node *s, Node* t)
	{
		s->touch_flag=1;
		int size=s->out_conn.size();
		for(int i=0;i<size;i++)
		{
			Node* n=s->out_conn[i]->out_node;
			if (n->touch_flag)
				continue;

			if (n==t || is_path(n,t))
				return true;
		}
		return false;
	}

	int depth()
	{
		flush();
		int mx=0;
		for(int i=0;i<inputs.size();i++)
		{
			int temp=depth(inputs[i],0);
			if (temp>mx)
				mx=temp;
		}
		return mx;
	}

	int depth(Node* k,int c)
	{
		if (k->output)
			return c;

		int mx=0;
		for(int i=0;i<k->out_conn.size();i++)
		{
			int temp=depth(k->out_conn[i]->out_node,c+1);
			if (temp>mx)
				mx=temp;
		}
		return mx;
	}

	void flush()
	{
		for(int c=0;c<nodes.size();c++)
			nodes[c]->flush();
	}
	void flush_connections()
	{
		for(int c=0;c<connections.size();c++)
			connections[c]->flush();
	}
	void load_inputs(double* inp)
	{
		for(int c=0;c<inputs.size();c++)
			inputs[c]->set_output(inp[c]);
	}
	void get_outputs(double* out)
	{
		for(int c=0;c<outputs.size();c++)
			out[c]=outputs[c]->get_output();
	}
	void activate()
	{
		for(int c=0;c<nodes.size();c++)
			nodes[c]->update();
	}

};
class xordomain:public domain
{
public:
	virtual void evaluate(individual* ind,data_record* dr=NULL)
	{
		double inps[4][2]={ {0.0,0.0}, {0.0,1.0}, {1.0,0.0}, {1.0,1.0} };
		double out[4]= {0.0,1.0,1.0,0.0};
		CPPN* c = (CPPN*)ind;
		double err=0.0;
		for(int x=0;x<4;x++)
		{
		double netout = c->query_net(inps[x]);
		double delta = out[x]-netout;
		delta*=delta;
		err+=delta;
		}

		ind->fitness=(4.01-err);
	}
};



class boxdomain:public domain
{
    public:
    double inputs[10000];
    double outputs[100];
    
    boxdomain()
    {
        ifstream inpfile("boxinput.txt");
        ifstream outfile("boxoutput.txt");
        int inpcount=0;
        if (!inpfile.is_open())
        {
            cout << "wtf" << endl;
        }

        while(!inpfile.eof())
        {
            inpfile >> inputs[inpcount];
            inpcount++;
        }
        int outcount=0;
        while(!outfile.eof())
        {
            outfile >> outputs[outcount];
            outcount++;
        }
    } 
    
    virtual void evaluate(individual* ind,data_record* dr=NULL)
    {
        int size=5;
        double err=0.0;
        Network* net=(Network*)ind;
        for(int x=0;x<8;x++)
        {
            net->inputs[0]->load_in(&inputs[size*size*x]);
            for(int k=0;k<10;k++)
                net->activate();
            vector<int> out = net->outputs[0]->max_activation();
            //cout << out[0] << " " << out[1] << endl;
            double d1 = out[0]-outputs[2*x];
            double d2 = out[1]-outputs[2*x+1];
            err+= d1*d1+d2*d2;
        }
        //cout << "Error:" << err << endl;
        ind->fitness = (8*size*size)*1.0 - err;
    }
};
#endif
