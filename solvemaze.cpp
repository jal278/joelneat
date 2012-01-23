////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// STL A* Search implementation
// (C)2001 Justin Heyes-Jones
//
// Finding a path on a simple grid maze
// This shows how to do shortest path finding using A*

////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "stlastar.h" // See header for copyright and usage information

#include <iostream>
#include <fstream>
#include <math.h>

#define DEBUG_LISTS 0
#define DEBUG_LIST_LENGTHS_ONLY 0
using namespace std;

// Global data

// The world map

int MAP_WIDTH = 64;
int MAP_HEIGHT = 64;

static double *map;

void out_array(char* fn,double* m) {
 ofstream ofile(fn);
 for(int y=0;y<MAP_HEIGHT;y++) 
 {
  for(int x=0;x<MAP_WIDTH;x++)
  {
   ofile << m[y*MAP_WIDTH+x];
  }
   ofile << endl;
 }
}

// map helper functions

int GetMap( int x, int y )
{

	if( x < 0 ||
	    x >= MAP_WIDTH ||
		 y < 0 ||
		 y >= MAP_HEIGHT
	  )
	{
		return 9;	 
	}

	if(map[(y*MAP_WIDTH)+x]==1.0)  return 9;
	return 1;
}



// Definitions

class MapSearchNode
{
public:
	unsigned int x;	 // the (x,y) positions of the node
	unsigned int y;	
	
	MapSearchNode() { x = y = 0; }
	MapSearchNode( unsigned int px, unsigned int py ) { x=px; y=py; }

	float GoalDistanceEstimate( MapSearchNode &nodeGoal );
	bool IsGoal( MapSearchNode &nodeGoal );
	bool GetSuccessors( AStarSearch<MapSearchNode> *astarsearch, MapSearchNode *parent_node );
	float GetCost( MapSearchNode &successor );
	bool IsSameState( MapSearchNode &rhs );

	void PrintNodeInfo(); 


};

bool MapSearchNode::IsSameState( MapSearchNode &rhs )
{
	// same state in a maze search is simply when (x,y) are the same
	if( (x == rhs.x) &&
		(y == rhs.y) )
	{
		return true;
	}
	else
	{
		return false;
	}

}

void MapSearchNode::PrintNodeInfo()
{
	cout << "Node position : (" << x << ", " << y << ")" << endl;
}

// Here's the heuristic function that estimates the distance from a Node
// to the Goal. 

float MapSearchNode::GoalDistanceEstimate( MapSearchNode &nodeGoal )
{
	float xd = fabs(float(((float)x - (float)nodeGoal.x)));
	float yd = fabs(float(((float)y - (float)nodeGoal.y)));

	return xd + yd;
}

bool MapSearchNode::IsGoal( MapSearchNode &nodeGoal )
{

	if( (x == nodeGoal.x) &&
		(y == nodeGoal.y) )
	{
		return true;
	}

	return false;
}

// This generates the successors to the given Node. It uses a helper function called
// AddSuccessor to give the successors to the AStar class. The A* specific initialisation
// is done for each node internally, so here you just set the state information that
// is specific to the application
bool MapSearchNode::GetSuccessors( AStarSearch<MapSearchNode> *astarsearch, MapSearchNode *parent_node )
{

	int parent_x = -1; 
	int parent_y = -1; 

	if( parent_node )
	{
		parent_x = parent_node->x;
		parent_y = parent_node->y;
	}
	

	MapSearchNode NewNode;

	// push each possible move except allowing the search to go backwards

	if( (GetMap( x-1, y ) < 9) 
		&& !((parent_x == x-1) && (parent_y == y))
	  ) 
	{
		NewNode = MapSearchNode( x-1, y );
		astarsearch->AddSuccessor( NewNode );
	}	

	if( (GetMap( x, y-1 ) < 9) 
		&& !((parent_x == x) && (parent_y == y-1))
	  ) 
	{
		NewNode = MapSearchNode( x, y-1 );
		astarsearch->AddSuccessor( NewNode );
	}	

	if( (GetMap( x+1, y ) < 9)
		&& !((parent_x == x+1) && (parent_y == y))
	  ) 
	{
		NewNode = MapSearchNode( x+1, y );
		astarsearch->AddSuccessor( NewNode );
	}	

		
	if( (GetMap( x, y+1 ) < 9) 
		&& !((parent_x == x) && (parent_y == y+1))
		)
	{
		NewNode = MapSearchNode( x, y+1 );
		astarsearch->AddSuccessor( NewNode );
	}	

	return true;
}

// given this node, what does it cost to move to successor. In the case
// of our map the answer is the map terrain value at this node since that is 
// conceptually where we're moving

float MapSearchNode::GetCost( MapSearchNode &successor )
{
	return (float) GetMap( x, y );

}


// Main

/*
int main( int argc, char *argv[] ) {
vector<int> k=solve_maze(map2,20,20);
for(int x=0;x<k.size();x+=2) {
 cout << k[x] << " " << k[x+1] << endl;
}
return 0;
}
*/

//vector<float>
void solve_maze(double* m,int width,int height,int& steps,vector<int>* path)
{
 vector<int> path2;
 if(path==NULL) path=&path2;
 vector<float> d;
 MAP_WIDTH=width;
 MAP_HEIGHT=height;
 map=m;
 AStarSearch<MapSearchNode> astarsearch;

		// Create a start state
		MapSearchNode nodeStart;
		nodeStart.x = (MAP_WIDTH-1) / 2;
		nodeStart.y = 0; 

		// Define the goal state
		MapSearchNode nodeEnd;
		nodeEnd.x = (MAP_WIDTH-1) /2;						
		nodeEnd.y = MAP_HEIGHT-1; 
		
		// Set Start and goal states
		
		astarsearch.SetStartAndGoalStates( nodeStart, nodeEnd );

		unsigned int SearchState;
		unsigned int SearchSteps = 0;

		do
		{
			SearchState = astarsearch.SearchStep();

			SearchSteps++;
                        if(SearchSteps>4096) {
                                astarsearch.CancelSearch();
                                cout << "too many search steps" << endl;
                        }

	#if DEBUG_LISTS

			cout << "Steps:" << SearchSteps << "\n";

			int len = 0;

			cout << "Open:\n";
			MapSearchNode *p = astarsearch.GetOpenListStart();
			while( p )
			{
				len++;
	#if !DEBUG_LIST_LENGTHS_ONLY			
				((MapSearchNode *)p)->PrintNodeInfo();
	#endif
				p = astarsearch.GetOpenListNext();
				
			}

			cout << "Open list has " << len << " nodes\n";

			len = 0;

			cout << "Closed:\n";
			p = astarsearch.GetClosedListStart();
			while( p )
			{
				len++;
	#if !DEBUG_LIST_LENGTHS_ONLY			
				//p->PrintNodeInfo();
	#endif			
				p = astarsearch.GetClosedListNext();
			}

			cout << "Closed list has " << len << " nodes\n";
	#endif

		}
		while( SearchState == AStarSearch<MapSearchNode>::SEARCH_STATE_SEARCHING );

		if( SearchState == AStarSearch<MapSearchNode>::SEARCH_STATE_SUCCEEDED )
		{
			//cout << "Search found goal state\n";

				MapSearchNode *node = astarsearch.GetSolutionStart();

	#if DISPLAY_SOLUTION
				cout << "Displaying solution\n";
	#endif
				int steps = 0;
                                        path->push_back(node->x);
                                        path->push_back(node->y);
				//node->PrintNodeInfo();
				for( ;; )
				{
					node = astarsearch.GetSolutionNext();

					if( !node )
					{
						break;
					}
                                        path->push_back(node->x);
                                        path->push_back(node->y);
					//node->PrintNodeInfo();
					steps ++;
				
				};

				//cout << "Solution steps " << steps << endl;

				// Once you're done with the solution you can free the nodes up
				astarsearch.FreeSolutionNodes();

	
		}
		else if( SearchState == AStarSearch<MapSearchNode>::SEARCH_STATE_FAILED ) 
		{
			//cout << "Search terminated. Did not find goal state\n";
		
		}

		// Display the number of loops the search went through
		//cout << "SearchSteps : " << SearchSteps << "\n";

	astarsearch.EnsureMemoryFreed();
        //steps=SearchSteps;	
        steps = path->size();

if(false) {
    int stepsize=(path->size())/17;
    if(stepsize%1==1) stepsize++;
    for(int k=stepsize;k<stepsize*17;k+=stepsize)
    {
     d.push_back((*path)[k]);
     d.push_back((*path)[k+1]);
    }
}
if(false) {
 if(path->size()>0) {
 int stepsize=SearchSteps/17;
 if(stepsize%1==1) stepsize++;
 for(int k=stepsize;k<stepsize*17;k+=stepsize)
 {
  d.push_back(astarsearch.xc[k]);
  d.push_back(astarsearch.yc[k]);
 }
 }
}

	return; // d;
}
