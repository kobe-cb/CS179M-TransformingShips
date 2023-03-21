#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <set>
#include <queue>
#include <utility> 

struct container{
    double weight;
    std::string name;
};

container* newContainer(double weight)
{
    container* newContainer = new container();
    newContainer->weight = weight;
    return newContainer;
}

struct Node{
    std::pair<int, int> beforeCoords;
    std::pair<int, int> currentCoords;
    double smallestDifference;
    int cost;
    Node* previous;
    std::vector<std::vector<container*>> CurrentGrid;
};
 
Node* newNode(std::vector<std::vector<container*>> &CurrentGrid, Node* shipGrid)
{
    Node* newNode = new Node();
    newNode->previous = shipGrid;
    newNode->CurrentGrid = CurrentGrid;
    return newNode;
}

Node* swapContainers(Node* shipGrid, int pos1, int pos2, int pos3, int pos4)
{
    container* temp;
    container* temp2;

    temp = shipGrid->CurrentGrid[pos1][pos2];
    temp2 = shipGrid->CurrentGrid[pos3][pos4];

    shipGrid->CurrentGrid[pos1][pos2] = temp2;
    shipGrid->CurrentGrid[pos3][pos4] = temp;

    return shipGrid;
}

struct Heuristic // comparator class for constructing the priority queue
{
    bool operator()(const Node*a, const Node* b)
    {
        return ((a->cost + a->smallestDifference) > (b->cost+ b->smallestDifference)); 
    }
};

int getCost(int pos1, int pos2, int pos3, int pos4)
{
    return std::abs(pos1-pos3)+std::abs(pos2-pos4);
}

void printGrid(Node* shipGrid)
{
    if (shipGrid == nullptr)
    {
        return;
    }

    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            std::cout<<shipGrid->CurrentGrid[i][j]->weight<<" ";
            if(j == 5)
            {
                std::cout<<" |  ";
            }
        }

        std::cout<<"\n";
    }
    std::cout<<"\n";
}

void printAnswer(Node* shipGrid)
{
    if (shipGrid != nullptr)
    {
        printAnswer(shipGrid->previous);
        if (shipGrid->previous != nullptr)
        {
            std::cout<<"Move container at ("<<shipGrid->beforeCoords.second<<","<<shipGrid->beforeCoords.first<<") to ("<<shipGrid->currentCoords.second<<","<<shipGrid->currentCoords.first<<")\n\n";
        }
        else
        {
            std::cout<<"Start\n\n";
        }
        printGrid(shipGrid);
    }
}

double leftsideSum(Node* shipGrid)
{
    double left = 0;
    for (int i = 0; i < 8; i++)
    {
        for(int j = 0; j < 6; j++)
        {
            if (shipGrid->CurrentGrid[i][j]->weight != -1)
            {
                left += shipGrid->CurrentGrid[i][j]->weight;
            }
        }
    }
    return left;
}

double rightsideSum(Node* shipGrid)
{
    double right = 0;
    for (int i = 0; i < 8; i++)
    {
        for(int j = 6; j < 12; j++)
        {
            if (shipGrid->CurrentGrid[i][j]->weight != -1)
            {
                right += shipGrid->CurrentGrid[i][j]->weight;
            }
        }
    }
    return right;
}

bool isBalanced(Node* shipGrid)
{
    double left = 0;
    double right = 0;
    double max = 0;
    double min = 0;

    left = leftsideSum(shipGrid);
    right = rightsideSum(shipGrid);
    //std::cout<<"Left side weighs "<<left<<" and Right side weighs "<<right<<"\n";
    max = std::max(left, right);
    min  = std::min(left,right);

    return ( (max-min) <= (max/10.0));
}

int getTopofColumn(Node* shipGrid, int whichColumn)
{
    for (int i = 0; i < 8; i++)
    {
        if (shipGrid->CurrentGrid[i][whichColumn]->weight != 0)
        {
            return i-1;
        }
    }
    return 7;

}

void makeBalanced(Node* shipGrid)  
{
    int NodeYPosition;
    int NodeXPosition; 
    int size;
    int temp;
    bool Balanced = false;
    Node* tempNode;

    int count = 0;

    std::set<std::vector<std::vector<double>>> dupeTrack;
    std::set<std::vector<std::vector<double>>>::iterator itr;
    std::vector<std::vector<double>> testOutput;
    std::vector<std::vector<double>> DupeGrid(8, std::vector<double>(12));

    std::priority_queue<Node*, std::vector<Node*>, Heuristic> queue;

    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            DupeGrid[i][j] = shipGrid->CurrentGrid[i][j]->weight;
        }   
    }

    dupeTrack.insert(DupeGrid);
    
    queue.push(shipGrid);

    while (!queue.empty())
    {
        shipGrid = queue.top();
        queue.pop();

        if(isBalanced(shipGrid))
        {
            printAnswer(shipGrid);
            std::cout<<"\nEstimated cost = "<<shipGrid->cost<<" minutes\n";
            std::cout<<"Ship is balanced Now\n\n";
            return;
        }

        for (int j  = 0; j < 12; j++)
        {
           
            NodeXPosition = j;
            NodeYPosition = getTopofColumn(shipGrid, NodeXPosition)+1;

            if (NodeYPosition == 8)//if column is all 0's
            {
                NodeYPosition = 7;
            }
        
            for (int i = 0; i < 12; i++)
            {
                if (i != NodeXPosition)
                {
                    temp = getTopofColumn(shipGrid, i);
                    if (temp > 0)
                    {
                        
                        //std::cout<<"\nNode swap "<< NodeXPosition<<","<<NodeYPosition<<" with "<<i<<","<<temp<<" By putting "<<shipGrid->CurrentGrid[NodeYPosition][NodeXPosition]->weight<<" at position "<< i<<","<< temp<<"\n";

                        swapContainers(shipGrid, temp, i, NodeYPosition, NodeXPosition);

                        for (int i = 0; i < 8; i++)
                        {
                            for (int j = 0; j < 12; j++)
                            {
                                DupeGrid[i][j] = shipGrid->CurrentGrid[i][j]->weight;
                            }   
                        }

                        size = dupeTrack.size();
                        dupeTrack.insert(DupeGrid);
                        if (!(size == dupeTrack.size()))//if it isn't a dupe
                        {  
                            tempNode = newNode(shipGrid->CurrentGrid, shipGrid);
                            tempNode->cost = shipGrid->cost + getCost(temp, i, NodeYPosition, NodeXPosition);
                            tempNode->smallestDifference = std::abs(leftsideSum(tempNode) - rightsideSum(tempNode));
                            tempNode->currentCoords.first =  i + 1;
                            tempNode->currentCoords.second = std::abs(7-temp) + 1;
                            tempNode->beforeCoords.first = NodeXPosition+1;
                            tempNode->beforeCoords.second = std::abs(7-NodeYPosition)+1; 
                            queue.push(tempNode);
                        }

                        swapContainers(shipGrid, temp, i, NodeYPosition, NodeXPosition);
                        
                    }
                }
            }
            
        }

    }
    
}

int main()
{
    std::vector<container*> temp;
    std::vector<std::vector<container*>> shipGrid;
    Node* tempNode;

    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            temp.push_back(newContainer(0));
        }   
        shipGrid.push_back(temp);
        temp.clear();
    }

    shipGrid[7][0]->weight = -1;

    shipGrid[3][3]->weight = 50;
    shipGrid[4][3]->weight = 50;
    shipGrid[5][3]->weight = 10;
    shipGrid[6][3]->weight = 1;
    shipGrid[7][3]->weight = 1;
    shipGrid[7][9]->weight = 50;
    shipGrid[6][9]->weight = 50;

    shipGrid[7][11]->weight = -1;
    
    /*{
        {0,0,0,0,0,0,  0,0,0,0,0,0},
        {0,0,0,0,0,0,  0,0,0,0,0,0},
        {0,0,0,0,0,0,  0,0,0,0,0,0},
        {0,0,0,50,0,0,  0,0,0,0,0,0},
        {0,0,0,50,0,0,  0,0,0,0,0,0},
        {0,0,0,10,0,0,  0,0,0,0,0,0},
        {0,0,0,1,0,0,  0,0,0,50,0,0},
        {-1,0,0,1,0,0,  0,0,0,50,0,-1}
    };*/

    
    tempNode = newNode(shipGrid,nullptr);
    tempNode->cost = 0;
    //printGrid(tempNode);
    std::cout<<"\n";

    if(isBalanced(tempNode))
    {
        std::cout<<"Ship is balanced\n";
    }
    else
    {
        std::cout<<"Ship is not balanced\n\n";
        makeBalanced(tempNode);
        
    }
    
    return 0;
}


/*
for (itr = dupeTrack.begin(); itr != dupeTrack.end(); itr++)
    {
        testOutput = *itr;

        count++;
    
        for (int i = 0; i <testOutput.size();i++)
        {
            for (int j = 0; j < testOutput[i].size(); j ++)
            {
                std::cout<<testOutput[i][j]->weight<<" ";
            }

            std::cout<<"\n";
        }

        std::cout<<"\n";
    }
    
    std::cout<<count;
*/