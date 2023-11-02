#include <Node.hpp>
#include <unordered_map>

using namespace std;

vector<int> get_label_frequencies(Dataframe &df)
{
    unordered_map<int, int> map;
    for (DataFrame::const_iterator it = df.cbegin(); it != df.cend(); ++it) {
        label = (*it).back();
        if (map.find(label) == map.end()) {
            map[label] = 1;
        } else {
            map[label] += 1;
        }
    }
}

double calc_entropy(DataFrame &df)
{
    
}

int calc_feature(DataFrame &df)
{

}

double calc_value(DataFrame &df)
{

}