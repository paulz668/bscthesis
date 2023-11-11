#include <iostream>
#include <src/lib/Node.hpp>

using namespace std;

int main() 
{
    DataFrame df = {
        {1.0, 2.0, 0.0},
        {4.0, 5.0, 1.0},
        {7.0, 8.0, 2.0}
    };
    Node node(df);
    cout << node.get_entropy() << endl;
    return EXIT_SUCCESS;
}