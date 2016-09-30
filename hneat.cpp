// hneat.cpp : Defines the entry point for the console application.
//

//#include "stdafx.h"
#include <vector>
#include <algorithm>
#include <time.h>
using namespace std;
#include "hneat.h"

static double transform(double i)
{
	return (double)(((int)((i*1000)+.5))/1000.0);
}

void Network::fix_weights()
{
for(int x=0;x<cppns.size();x++)
	cppns[x]->fix_weights();
}

void CPPN::fix_weights()
{
trivial_weight=transform(trivial_weight);
for(int x=0;x<connections.size();x++)
	connections[x]->weight=transform(connections[x]->weight);
}

void Network::create()
{
for(int x=0;x<cppns.size();x++)
	cppns[x]->generate_weight_matrix();
fix_weights();
created=true;
}

Network::~Network()
{
        for(int x=0;x<cppns.size();x++)
            delete cppns[x];

        for(int x=0;x<substrates.size();x++)
            delete substrates[x];
}
species::species(individual* ind)
	{
		prototype=ind->make_copy();
		members.push_back(ind);
	}
	
species::~species()
	{
        delete prototype;
    }



//bastardized version of CPPN::distance
double Network::distance(individual* ind)
{
		Network* c2 = (Network*)ind;
		int excess=0;
		int disjoint=0;
		int matching=0;
		double weight_dif=0.0;

		Network* c1 = this;
		long int c1inno=0;
		long int c2inno=0;
		int c1index=0;
		int c2index=0;
		
		int c1size=c1->cppns.size();
		int c2size=c2->cppns.size();
		
		int c1max=c1->cppns[c1size-1]->innovation;
		int c2max=c2->cppns[c2size-1]->innovation;

		while(c1index<c1size && c2index<c2size)
		{
			c1inno=c1->cppns[c1index]->innovation;
			c2inno=c2->cppns[c2index]->innovation;
			if(c1inno==c2inno)
			{
				matching++;
				double d=c1->cppns[c1index]->distance(c2->cppns[c2index]);
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
		double dif=weight_dif*0.5+excess*2.0+disjoint*1.0;
		//cout << matching << " " << dif << endl;
		return dif;
}

individual* Network::make_copy()
{
	vector<Substrate*> subs;
	vector<CPPN*> cppn;

	subs.reserve(10);
	cppn.reserve(10);

	for(int i=0;i<substrates.size();i++)
		subs.push_back(substrates[i]->Copy());

	for(int i=0;i<cppns.size();i++)
		cppn.push_back(cppns[i]->Copy(subs));

	individual* newnet=(individual*)new Network(subs,cppn);

	newnet->fitness=fitness;
	newnet->behavior=behavior;
	return newnet;
}
void Network::change()
{
	for(int i=0;i<cppns.size();i++)
		cppns[i]->change();
}
 void Network::mutate() { 

	    //add_link mutation    	
    		if (chance(0.00))
			mutate_add_CPPN();
		
		//add_node mutation
		if (chance(0.00))
			mutate_add_substrate();


		for(int x=0;x<cppns.size();x++)
			if(chance(0.4))
				cppns[x]->mutate();
		
	
}

//bastardized copy of mutate_add_node from CPPN
void Network::mutate_add_substrate()
	{
		bool found=false;
		CPPN* to_split;
		
		//don't want to split bias connections
		while(!found)
		{
		
		found=true;

		//choose random connection
		to_split = cppns[randint(0,cppns.size())];
		
		if (to_split->in_substrate->bias)
			found=false;
		}

		//TODO: we don't have to limit ourselves to this, many more possibilites...
		//but for now...copy resolution of one of the two nodes
		vector<int> res;
		back_insert_iterator< vector<int> > it(res);
		vector<int> *to_copy;

		if(chance(0.5))
		{

			if(chance(0.5))
				to_copy=(&to_split->in_substrate->resolutions);
			else
				to_copy=(&to_split->out_substrate->resolutions);
			copy(to_copy->begin(),to_copy->end(),it);
	
		}
		else
		{
			vector<int>* n=new vector<int>;
			if(chance(0.5))
			{
				res.push_back(5);
				res.push_back(5);
			}
			else
			{
				res.push_back(3);
				res.push_back(3);
				res.push_back(3);
			}
			to_copy=n;
		}		

		//create new node
		Substrate* newnode = new Substrate(res,false,false,false,Singleton::next_inno());
		
		/*
		CPPN* c1 = to_split->Copy(substrates);
		c1->out_substrate=newnode;
		c1->innovation=Singleton::next_inno();
		*/

       		 CPPN* c1 = new CPPN(to_split->in_substrate,newnode,Singleton::next_inno());
		CPPN* c2 = new CPPN(newnode,to_split->out_substrate,Singleton::next_inno(),true);
        
        
		//TODO:
		//Maybe make c1 an exact copy of to_split
		//Maybe mutate c2 to minimize impact (e.g. reduce magnitude of weights)

			
		substrates.push_back(newnode);
		cppns.push_back(c1);
		cppns.push_back(c2);
	}
	//bastardized copy of mutate_add_link from CPPN
	void Network::mutate_add_CPPN()
	{
		int num_tries=30;
		bool found=false;
		Substrate *n1,*n2;
		while(num_tries>0 && !found)
		{
			found=true;
			
			n1=substrates[randint(0,substrates.size())];
			n2=substrates[randint(0,substrates.size())];
			
			if (n2->input)
				found=false;

			if (n2->bias)
				found=false;

			if (n1==n2)
				found=false;
			
			for(int x=0;x<cppns.size();x++)
				if (cppns[x]->in_substrate==n1 &&
					cppns[x]->out_substrate==n2)
						found=false;

			/*
			if (recurrent(n1,n2))
				found=false;
			*/
			num_tries--;
		}

		//unsuccessful
		if (!found)
			return;

		CPPN* k = new CPPN(n1,n2,Singleton::next_inno());
		
		//add the new connection
		cppns.push_back(k);
	}

Connection* Connection::Copy(vector<Node*> nlist)
	{
		Node* in;
		Node* out;
	
		for(int x=0;x<nlist.size();x++)
		{
			if (nlist[x]->innovation==in_node->innovation)
				in=nlist[x];
			if (nlist[x]->innovation==out_node->innovation)
				out=nlist[x];
		}

		return new Connection(in,out,weight,innovation);
	}

Network* Network::Copy()
	{
		vector<Substrate*> s;
		vector<CPPN*> c;

		s.reserve(10);
		c.reserve(10);
		for(int x=0;x<substrates.size();x++)
			s.push_back(substrates[x]->Copy());
		for(int x=0;x<cppns.size();x++) 
			c.push_back(cppns[x]->Copy(s));
		return new Network(s,c);
	}

void Network::flush()
{
if(!created)
 create();
for(int x=0;x<substrates.size();x++)
 substrates[x]->flush();
}
void Network::activate()
{
if(!created)
	create();
for(int x=0;x<substrates.size();x++)
	substrates[x]->update();
}

void Substrate::update()
{
		if (bias)
		{
			activation=1.0;
			return;
		}
		if (input)
			return;

		//reset summations
		sum=0.0;

		for(int x=0;x<num_neurons;x++)
			sum_matrix[x]=bias_matrix[x]; //0.0;

		//accumulate connections
		for(int x=0;x<in_conn.size();x++)
			in_conn[x]->update();

		//activate neurons
		for(int x=0;x<num_neurons;x++)
			activation_matrix[x]=sigmoid(sum_matrix[x]);

		activation=sigmoid(sum);
}



TiXmlElement* Network::create_xml()
{
	TiXmlElement* net_node = new TiXmlElement("network");
	TiXmlElement* cppns_node = new TiXmlElement("CPPNs");
	TiXmlElement* substrate_node = new TiXmlElement("substrates");

		char outstring[100000];		
		sprintf(outstring,"%f",fitness);
		if(noveltypoint!=NULL)
			sprintf(outstring,"%f",noveltypoint->fitness);
		net_node->SetAttribute("fitness",outstring);
		sprintf(outstring,"%f",behavior);
		net_node->SetAttribute("behavior",outstring);


	for(int i=0;i<cppns.size();i++)
	{
		cppns_node->LinkEndChild(cppns[i]->create_xml());
	}

	for(int i=0;i<substrates.size();i++)
	{
		substrate_node->LinkEndChild(substrates[i]->create_xml());
	}

	net_node->LinkEndChild(substrate_node);
	net_node->LinkEndChild(cppns_node);

	return net_node;
}

Network* Network::load(TiXmlElement* net_xml)
{
	TiXmlElement* cppns_xml = net_xml->FirstChildElement("CPPNs");
	TiXmlElement* substrate_xml= net_xml->FirstChildElement("substrates");

	TiXmlElement* elem;

	vector<Substrate*> subs;
	vector<CPPN*> cppns;
	
	elem=substrate_xml->FirstChildElement("substrate");
	for(elem;elem;elem=elem->NextSiblingElement())
	{
		subs.push_back(Substrate::load(elem));
	}

	elem=cppns_xml->FirstChildElement("CPPN");
	for(elem;elem;elem=elem->NextSiblingElement())
	{
		cppns.push_back(CPPN::load(elem,subs));
	}
	Network* k = new Network(subs,cppns);
	k->fitness = atof(net_xml->Attribute("fitness"));
	k->behavior = atof(net_xml->Attribute("behavior"));
        return k;
}

int Network::complexity() {
int c=0;
for(int i=0;i<cppns.size();i++)
 c+=cppns[i]->complexity();
return c;
}
int CPPN::complexity() {
return nodes.size(); 
}

Network::Network(vector<Substrate*>& subs,vector<CPPN*>& cppn)
	{
		substrates.reserve(10);
		cppns.reserve(10);
		back_insert_iterator<vector<Substrate*> > s_iter (substrates);
		back_insert_iterator<vector<CPPN*> > c_iter (cppns);		
		copy(subs.begin(),subs.end(),s_iter);
		copy(cppn.begin(),cppn.end(),c_iter);

		created=false;
                
		for(int i=0;i<substrates.size();i++)
		{
			if (substrates[i]->input)
				inputs.push_back(substrates[i]);
			if (substrates[i]->output)
				outputs.push_back(substrates[i]);
		}
	}



	TiXmlElement* CPPN::create_xml()
	{
		char outstring[100000];
		
		TiXmlElement* cppn_node= new TiXmlElement("CPPN");
		
		sprintf(outstring,"%d",trivial);
		cppn_node->SetAttribute("trivial",outstring);

		sprintf(outstring,"%0.5f",trivial_weight);
		cppn_node->SetAttribute("trivial_weight",outstring);

		sprintf(outstring,"%d",dim);
		cppn_node->SetAttribute("dimensionality",outstring);
                if(in_substrate!=NULL && out_substrate !=NULL) {
                sprintf(outstring,"%ld",in_substrate->innovation);
		cppn_node->SetAttribute("in_substrate",outstring);

		sprintf(outstring,"%ld",out_substrate->innovation);
		cppn_node->SetAttribute("out_substrate",outstring);

                }
		sprintf(outstring,"%ld",innovation);
		cppn_node->SetAttribute("innovation",outstring);

		sprintf(outstring,"%f",fitness);
		if(noveltypoint!=NULL)
			sprintf(outstring,"%f",noveltypoint->fitness);
		cppn_node->SetAttribute("fitness",outstring);
		sprintf(outstring,"%f",behavior);
		cppn_node->SetAttribute("behavior",outstring);
		
                TiXmlElement* nodes_xml = new TiXmlElement("nodes");
		for(int x=0;x<nodes.size();x++)
			nodes_xml->LinkEndChild(nodes[x]->create_xml());

		TiXmlElement* connect_xml = new TiXmlElement("connections");
		for(int x=0;x<connections.size();x++)
			connect_xml->LinkEndChild(connections[x]->create_xml());

		cppn_node->LinkEndChild(nodes_xml);
		cppn_node->LinkEndChild(connect_xml);
		
		return cppn_node;
	}

Connection::Connection(Node* in_node,Node* out_node,double weight, long int inn):in_node(in_node),out_node(out_node),weight(weight),innovation(inn)
	{
		in_node->out_conn.push_back(this);
		out_node->in_conn.push_back(this);
	}

	TiXmlElement* Connection::create_xml()
	{
		char outstring[100];
		
		TiXmlElement* conn_xml= new TiXmlElement("connection");
		
		sprintf(outstring,"%ld",in_node->innovation);
		conn_xml->SetAttribute("in_node",outstring);

		sprintf(outstring,"%ld",out_node->innovation);
		conn_xml->SetAttribute("out_node",outstring);

		sprintf(outstring,"%0.5lf",weight);
		conn_xml->SetAttribute("weight",outstring);

		sprintf(outstring,"%ld",innovation);
		conn_xml->SetAttribute("innovation",outstring);

		return conn_xml;
	}

	Connection* Connection::load(TiXmlElement* node_xml,vector<Node*> nodes)
	{
		int in_inno=atol(node_xml->Attribute("in_node"));
		int out_inno=atol(node_xml->Attribute("out_node"));
		double weight=atof(node_xml->Attribute("weight"));
		int innovation=atol(node_xml->Attribute("innovation"));

		Node* in_node;
		Node* out_node;
		//match nodes
		for(int x=0;x<nodes.size();x++)
		{
			if (in_inno==nodes[x]->innovation)
				in_node=nodes[x];
			if (out_inno==nodes[x]->innovation)
				out_node=nodes[x];
		}

		Connection* k= new Connection(in_node,out_node,weight,innovation);
		return k;
	}

void Connection::update() { value=in_node->get_output()*weight; }

Singleton* Singleton::GetInstance()
{
    static Singleton inst;
    return &inst;
}

void test_representation()
{
	vector<Node*> node_list;
	vector<Connection*> connection_list;
	vector<Substrate*> substrate_list;
	vector<CPPN*> cppn_list;

	node_list.push_back(new Node(true,false,false,0,10));
	node_list.push_back(new Node(false,false,true,0,11));
	node_list.push_back(new Node(false,true,false,0,12));
	node_list.push_back(new Node(false,false,false,0,13));
	connection_list.push_back(new Connection(node_list[0],node_list[3],0.1,14));
	connection_list.push_back(new Connection(node_list[3],node_list[2],0.1,15));
	connection_list.push_back(new Connection(node_list[0],node_list[2],0.3,16));
	connection_list.push_back(new Connection(node_list[1],node_list[2],0.25,17));
	vector<int> rsource;
	vector<int> rtarget;
	rtarget.push_back(50);
	Substrate* source=new Substrate(rsource,true,false,false,3);
	Substrate* target=new Substrate(rtarget,false,true,false,4);
	substrate_list.push_back(source);
	substrate_list.push_back(target);

	srand ( time(NULL) );

	CPPN* cppn= new CPPN(source,target,5,node_list,connection_list,1.0);
	double inp[2]={0.5,0.5};
	double out;

	cppn->flush();
	cppn->load_inputs(inp);
	
	cppn->activate();
	cppn->activate();
	cppn->activate();
	cppn->activate();
	cppn->activate();

	cppn->get_outputs(&out);
	cppn->save("blah.xml");

	//try to load xml file
	CPPN* newcppn = CPPN::load("blah.xml",substrate_list);

	cout << "distance1: " << newcppn->distance(cppn) << endl;

	for(int x=0;x<1000;x++)
		newcppn->mutate();

	cout << "distance2: " << newcppn->distance(cppn) << endl;

	newcppn->save("blah2.xml");

	cppn_list.push_back(cppn);
	Network* n= new Network(substrate_list,cppn_list);
	n->save("network.xml");

	Network* newnet = Network::load("network.xml");
	newnet->save("network2.xml");

	cout << "query out:" << newcppn->query_net(inp) << endl;

	cout << out << endl;
	cout << newcppn->depth() << endl;

	/*
	newnet->cppns[0]->generate_weight_matrix();
	for(int x=0;x<50;x++)
		cout << "weight " << x << " " << newnet->cppns[0]->weight_matrix[x] << endl;
	*/
	delete newnet;
	delete n;
	delete newcppn;
}
void test_evolve_simple()
{
    simpledom dom;
	population p(true);
	evolve *k;

	for(int x=0;x<250;x++)
		p.members.push_back(new simpleind());

	k=new evolve(&p,&dom);
	
	while(true)
		k->epoch(250);
}

void test_evolve_xor()
{
    xordomain dom;
	population p(true);
	evolve *k;

	vector<int> r1;
	vector<int> r2;
	r1.push_back(25);
	r1.push_back(25);
	Substrate* s = new Substrate(r1,true,false,false,0);
	Substrate* t = new Substrate(r2,false,true,false,1);
	CPPN* first=new CPPN(s,t,10);

	for(int x=0;x<250;x++)
	{
		CPPN* newcppn = (CPPN*)first->make_copy();
		newcppn->mutate_links();
		
		p.members.push_back((individual*)newcppn);
	}
	k=new evolve(&p,&dom);

	for(int x=0;x<100;x++)
		k->epoch(250);
}

void test_evolve_boxes()
{
	xordomain dom;
	population p(true);
	evolve *k;

	vector<int> r1;
	vector<int> r2;
	r1.push_back(5);
	r1.push_back(5);
	Substrate* s = new Substrate(r1,true,false,false,0);
	Substrate* t = new Substrate(r1,false,true,false,1);
	Substrate* b = new Substrate(r2,false,false,true,2);
	CPPN* first=new CPPN(s,t,10);
	CPPN* bias=new CPPN(b,t,Singleton::next_inno());
	
	vector<Substrate*> subs;
	vector<CPPN*> cppns;
	
	subs.push_back(s);
	subs.push_back(t);
	subs.push_back(b);
	
	cppns.push_back(first);
	cppns.push_back(bias);

        Network* orig = new Network(subs,cppns);  

	for(int x=0;x<250;x++)
	{
		Network* newnet = (Network*)orig->make_copy();
		p.members.push_back((individual*)newnet);
	}
	delete orig;

	k=new evolve(&p,&dom);
	
	int count=0;
	char fname[50];

        while(count<1)	{
        sprintf(fname,"gen%d.xml",count);
		k->epoch(250);
		
		count++;
	}
	k->p->save(fname);

	//system("pause");
	delete k;
}



