#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <set>
#include <queue>
#include <utility>
#include <fstream>
#include <numeric>
#include <cmath>

int CraneCost = 0;

struct container
{
    double weight;
    std::string name;
};

container *newContainer(double weight, std::string name)
{
    container *newContainer = new container();
    newContainer->weight = weight;
    newContainer->name = name;
    return newContainer;
}

struct Node
{
    std::pair<int, int> beforeCoords;
    std::pair<int, int> currentCoords;
    double smallestDifference;
    int cost;
    Node *previous;
    std::vector<std::vector<container *>> CurrentGrid;
};

Node *newNode(std::vector<std::vector<container *>> &CurrentGrid, Node *shipGrid)
{
    Node *newNode = new Node();
    newNode->previous = shipGrid;
    newNode->CurrentGrid = CurrentGrid;
    return newNode;
}

Node *swapContainers(Node *shipGrid, int pos1, int pos2, int pos3, int pos4)
{
    container *temp;
    container *temp2;

    temp = shipGrid->CurrentGrid[pos1][pos2];
    temp2 = shipGrid->CurrentGrid[pos3][pos4];

    shipGrid->CurrentGrid[pos1][pos2] = temp2;
    shipGrid->CurrentGrid[pos3][pos4] = temp;

    return shipGrid;
}

struct Heuristic // comparator class for constructing the priority queue
{
    bool operator()(const Node *a, const Node *b)
    {
        return ((a->cost) >= (b->cost));
    }
};

struct WeightHeuristic // comparator class for sift
{
    bool operator()(const container *a, const container *b)
    {
        return ((a->weight) < (b->weight));
    }
};

int getCost(int pos1, int pos2, int pos3, int pos4)
{
    return std::abs(pos1 - pos3) + std::abs(pos2 - pos4);
}

void printGrid(Node *shipGrid)
{
    if (shipGrid == nullptr)
    {
        return;
    }

    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            std::cout << shipGrid->CurrentGrid[i][j]->weight << " ";
            if (j == 5)
            {
                std::cout << " |  ";
            }
        }

        std::cout << "\n";
    }
    std::cout << "\n";
}

void printAnswer(Node *shipGrid, std::vector<std::string> &answerPath)
{
    std::string temp;

    if (shipGrid != nullptr)
    {
        printAnswer(shipGrid->previous, answerPath);
        if (shipGrid->previous != nullptr)
        {
            temp += "Move (";
            temp += std::to_string(shipGrid->beforeCoords.second);
            temp += ",";
            temp += std::to_string(shipGrid->beforeCoords.first);
            temp += ") to (";
            temp += std::to_string(shipGrid->currentCoords.second);
            temp += ",";
            temp += std::to_string(shipGrid->currentCoords.first);
            temp += ")";
            // std::cout<<temp<<"\n\n";
            // std::cout<< "\n"<<std::abs(shipGrid->previous->currentCoords.first - shipGrid->beforeCoords.first) + std::abs(shipGrid->previous->currentCoords.second - shipGrid->beforeCoords.second);
            // std::cout<<"\n"<<shipGrid->previous->currentCoords.first<<" and "<< shipGrid->beforeCoords.first<<std::endl;
            CraneCost += std::abs(shipGrid->beforeCoords.first - shipGrid->currentCoords.first) + std::abs(shipGrid->beforeCoords.second - shipGrid->currentCoords.second);
            answerPath.push_back(temp);
            // std::cout<<"Move ("<<shipGrid->beforeCoords.second<<","<<shipGrid->beforeCoords.first<<") to ("<<shipGrid->currentCoords.second<<","<<shipGrid->currentCoords.first<<")\n\n";
        }
        else
        {
            // std::cout<<"Start\n\n";
        }
        // printGrid(shipGrid);
    }
}

double leftsideSum(Node *shipGrid)
{
    double left = 0;
    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 6; j++)
        {
            if (shipGrid->CurrentGrid[i][j]->weight != -1)
            {
                left += shipGrid->CurrentGrid[i][j]->weight;
            }
        }
    }
    return left;
}

double rightsideSum(Node *shipGrid)
{
    double right = 0;
    for (int i = 0; i < 8; i++)
    {
        for (int j = 6; j < 12; j++)
        {
            if (shipGrid->CurrentGrid[i][j]->weight != -1)
            {
                right += shipGrid->CurrentGrid[i][j]->weight;
            }
        }
    }
    return right;
}

bool isBalanced(Node *shipGrid)
{
    double left = 0;
    double right = 0;
    double max = 0;
    double min = 0;

    left = leftsideSum(shipGrid);
    right = rightsideSum(shipGrid);
    // std::cout<<"Left side weighs "<<left<<" and Right side weighs "<<right<<"\n";
    max = std::max(left, right);
    min = std::min(left, right);

    return ((max - min) <= (max / 10.0));
}

int getTopofColumn(Node *shipGrid, int whichColumn)
{
    for (int i = 0; i < 8; i++)
    {
        if (shipGrid->CurrentGrid[i][whichColumn]->weight != 0)
        {
            return i - 1;
        }
    }
    return 7;
}

bool isSiftDone(Node *shipGrid, Node *endstate)
{
    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            if (shipGrid->CurrentGrid[i][j]->name != endstate->CurrentGrid[i][j]->name)
            {
                return false;
            }
        }
    }
    return true;
}

Node *calculateEndState(Node *shipGrid)
{
    std::priority_queue<container *, std::vector<container *>, WeightHeuristic> queue;
    container *temp;
    Node *tempNode = shipGrid;
    bool left = true;

    for (int i = 0; i < tempNode->CurrentGrid.size(); i++)
    {
        for (int j = 0; j < tempNode->CurrentGrid[i].size(); j++)
        {
            if (tempNode->CurrentGrid[i][j]->weight > 0)
            {
                temp = tempNode->CurrentGrid[i][j];
                queue.push(temp);
                temp = newContainer(0, "UNUSED");
                tempNode->CurrentGrid[i][j] = temp;
            }
        }
    }

    while (!queue.empty())
    {
        temp = queue.top();
        queue.pop();
        if (left == true)
        {
            for (int i = 7; i > -1; i--)
            {
                for (int j = 5; j > -1; j--)
                {
                    if (tempNode->CurrentGrid[i][j]->weight == 0)
                    {
                        tempNode->CurrentGrid[i][j] = temp;
                        left = false;
                        break;
                    }
                }

                if (left == false)
                {
                    break;
                }
            }
        }
        else if (left == false)
        {
            for (int i = 7; i > -1; i--)
            {
                for (int j = 6; j < 12; j++)
                {
                    if (tempNode->CurrentGrid[i][j]->weight == 0)
                    {
                        tempNode->CurrentGrid[i][j] = temp;
                        left = true;
                        break;
                    }
                }
                if (left == true)
                {
                    break;
                }
            }
        }
    }

    return tempNode;
}

int ManHatDis(Node *shipGrid, Node *endstate)
{
    int cost = 0;

    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            if (shipGrid->CurrentGrid[i][j]->weight > 0)
            {
                for (int k = 0; k < 8; k++)
                {
                    for (int h = 0; h < 12; h++)
                    {
                        if (shipGrid->CurrentGrid[i][j]->name == endstate->CurrentGrid[k][h]->name)
                        {
                            // std::cout<<i<<","<<j<<","<<k<<","<<h<<std::endl;
                            cost += std::abs(k - i) + std::abs(h - j);
                        }
                    }
                }
            }
        }
    }
    // std::cout<<cost<<std::endl;
    return cost;
}

void makeBalanced(Node *shipGrid, bool Sifting)
{
    int first;
    int second;
    std::string firstCoord;
    std::string secondCoord;
    int NodeYPosition;
    int NodeXPosition;
    int size;
    int temp;
    bool Balanced = false;
    Node *tempNode;
    Node *endstate = newNode(shipGrid->CurrentGrid, nullptr);

    int count = 0;

    if (Sifting == true)
    {
        calculateEndState(endstate);
    }

    int SiftCost = ManHatDis(shipGrid, endstate);

    std::ofstream outfile("./Instructions.txt");

    std::vector<std::string> answerPath;
    std::set<std::vector<std::vector<double>>> dupeTrack;
    std::set<std::vector<std::vector<double>>>::iterator itr;
    std::vector<std::vector<double>> testOutput;
    std::vector<std::vector<double>> DupeGrid(8, std::vector<double>(12));

    std::priority_queue<Node *, std::vector<Node *>, Heuristic> queue;

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

        if (isSiftDone(shipGrid, endstate) && Sifting == true)
        {
            // printGrid(shipGrid);
            printAnswer(shipGrid, answerPath);

            firstCoord.assign(answerPath[0], 6, 1);
            secondCoord.assign(answerPath[0], 8, 1);

            first = std::stoi(firstCoord);
            second = std::stoi(secondCoord);
            CraneCost += std::abs(9 - first) + std::abs(1 - second);
            CraneCost += std::abs(1 - shipGrid->currentCoords.first) + std::abs(9 - shipGrid->currentCoords.second);
            CraneCost -= std::abs(0 - first) + std::abs(0 - second);
            // std::cout<<"\nEstimated cost = "<<SiftCost + CraneCost<<" minutes\n\n";
            outfile << "Estimated cost = " << SiftCost + CraneCost << " minutes" << std::endl;
            // std::cout<<"Ship is balanced Now\n\n";
            for (int i = 0; i < answerPath.size(); i++)
            {
                outfile << answerPath[i] << std::endl;
            }
            return;
        }
        else if (isBalanced(shipGrid))
        {
            printAnswer(shipGrid, answerPath);

            firstCoord.assign(answerPath[0], 6, 1);
            secondCoord.assign(answerPath[0], 8, 1);

            first = std::stoi(firstCoord);
            second = std::stoi(secondCoord);

            CraneCost += std::abs(9 - first) + std::abs(1 - second);
            CraneCost += std::abs(1 - shipGrid->currentCoords.first) + std::abs(9 - shipGrid->currentCoords.second);
            CraneCost -= std::abs(0 - first) + std::abs(0 - second);
            // std::cout<<"\nEstimated cost = "<<shipGrid->cost+CraneCost<<" minutes\n\n";

            outfile << "Estimated cost = " << shipGrid->cost + CraneCost << " minutes" << std::endl;

            for (int i = 0; i < answerPath.size(); i++)
            {
                outfile << answerPath[i] << std::endl;
            }
            // std::cout<<"Ship is balanced Now\n\n";
            return;
        }

        for (int j = 0; j < 12; j++)
        {

            NodeXPosition = j;
            NodeYPosition = getTopofColumn(shipGrid, NodeXPosition) + 1;

            if (NodeYPosition == 8) // if column is all 0's
            {
                NodeYPosition = 7;
            }

            while (shipGrid->CurrentGrid[NodeYPosition][NodeXPosition]->weight == -1 && NodeYPosition > -1) // if there is negative ones
            {
                NodeYPosition--;
            }

            if (NodeYPosition > -1)
            {
                if (shipGrid->CurrentGrid[NodeYPosition][NodeXPosition]->weight > 0)
                {
                    for (int i = 0; i < 12; i++)
                    {
                        if (i != NodeXPosition)
                        {
                            temp = getTopofColumn(shipGrid, i);
                            if (temp > 0)
                            {

                                // std::cout<<"\nNode swap "<< NodeXPosition<<","<<NodeYPosition<<" with "<<i<<","<<temp<<" By putting "<<shipGrid->CurrentGrid[NodeYPosition][NodeXPosition]->weight<<" at position "<< i<<","<< temp<<"\n";

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
                                if (!(size == dupeTrack.size())) // if it isn't a dupe
                                {
                                    tempNode = newNode(shipGrid->CurrentGrid, shipGrid);
                                    if (Sifting == false)
                                    {
                                        tempNode->cost = shipGrid->cost + getCost(temp, i, NodeYPosition, NodeXPosition);
                                    }
                                    else if (Sifting == true)
                                    {
                                        tempNode->cost = ManHatDis(tempNode, endstate);
                                    }
                                    tempNode->smallestDifference = std::abs(leftsideSum(tempNode) - rightsideSum(tempNode));
                                    tempNode->currentCoords.first = i + 1;
                                    tempNode->currentCoords.second = std::abs(7 - temp) + 1;
                                    tempNode->beforeCoords.first = NodeXPosition + 1;
                                    tempNode->beforeCoords.second = std::abs(7 - NodeYPosition) + 1;
                                    // printGrid(tempNode);
                                    queue.push(tempNode);
                                }

                                swapContainers(shipGrid, temp, i, NodeYPosition, NodeXPosition);
                            }
                        }
                    }
                }
            }
        }
    }
}

bool isSubsetSum(std::vector<double> check, int n, int sum)
{

    if (sum == 0)
    {
        return true;
    }

    if (n == 0)
    {
        return false;
    }

    if (check[n - 1] > sum)
    {
        return isSubsetSum(check, n - 1, sum);
    }
    return isSubsetSum(check, n - 1, sum) || isSubsetSum(check, n - 1, sum - check[n - 1]);
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        std::cout << argv[0] << "lacks arguments.";
        return 1;
    }

    std::string fileName = argv[1];

    std::vector<double> check;
    std::vector<container *> temp;
    std::vector<std::vector<container *>> shipGrid;
    Node *tempNode;
    double reduce = 0;
    int lowerBound;
    int upperBound;
    int checksize;
    bool performSift = true;
    CraneCost = 0;

    for (int i = 0; i < 8; i++)
    {
        for (int j = 0; j < 12; j++)
        {
            temp.push_back(newContainer(0, "UNUSED"));
        }
        shipGrid.push_back(temp);
        temp.clear();
    }

    std::string yCoord;
    std::string xCoord;
    std::fstream myFile;
    std::string getWeight;
    std::string name;

    int posY;
    int posX;
    double weight;

    // myFile.open('./Manifest.txt', ...)
    myFile.open(fileName, std::ios::in);

    if (myFile.is_open())
    {
        std::string line;
        while (getline(myFile, line))
        {
            yCoord.assign(line, 1, 2);
            posY = std::stoi(yCoord); // Y coord

            xCoord.assign(line, 4, 2);
            posX = std::stoi(xCoord); // X coord

            name.assign(line, 18, std::string::npos);

            if (name == "NAN")
            {
                weight = -1;
            }
            else
            {
                getWeight.assign(line, 10, 5);
                weight = std::stod(getWeight); // weight of container
            }

            if (name != "UNUSED" && name != "NAN")
            {
                shipGrid[(7 - posY) + 1][posX - 1]->weight = weight;
                shipGrid[(7 - posY) + 1][posX - 1]->name.assign(name);
                check.push_back(weight);
            }
            if (name == "NAN")
            {
                shipGrid[(7 - posY) + 1][posX - 1]->weight = -1;
                shipGrid[(7 - posY) + 1][posX - 1]->name.assign("NAN");
            }
        }
        myFile.close();
    }
    else
    {
        std::cout << "\nFile Not found\n";
    }

    tempNode = newNode(shipGrid, nullptr);
    tempNode->cost = 0;
    printGrid(tempNode);
    std::cout << "\n";

    reduce = std::accumulate(check.begin(), check.end(), reduce);
    lowerBound = std::ceil((reduce / 2.0) * .95);
    upperBound = std::floor(((reduce / 2.0) * 1.05));
    checksize = check.size();

    for (int i = lowerBound; i < upperBound; i++)
    {
        if (isSubsetSum(check, checksize, i))
        {
            performSift = false;
        }
    }

    if (checksize < 2)
    {
        performSift = true;
    }

    if (performSift == false)
    {
        if (isBalanced(tempNode))
        {
            std::cout << "Ship is already balanced.\n";
        }
        else
        {
            std::cout << "Ship is not balanced.\nCalculating steps to balance the ship:";
            makeBalanced(tempNode, false);
        }
    }
    else
    {
        std::cout << "\nPerforming Sift\n";
        makeBalanced(tempNode, true);
    }
    return 0;
}
