#include <Node.hpp>
#include <algorithm>
#include <cmath>

using namespace std;

// calculate the relative label frequencies in the data using a DataFrame reference 
vector<double> get_label_frequencies(const DataFrame &df)
{
    vector<double> res = {0,0,0};
    size_t count = df.size();
    for (DataFrame::const_iterator it = df.cbegin(); it != df.cend(); ++it) {
        if ((*it).back() == 0) {
            res[0] += 1;
        } else if ((*it).back() == 1) {
            res[1] += 1;
        } else {
            res[2] += 1;
        }
    }
    transform(res.begin(), res.end(), res.begin(), [count](int &c){ return c/count; });
    return res;
}

// calculate the relative label frequencies in the data using start and end iterators
vector<double> get_label_frequencies(DataFrame::const_iterator beg, DataFrame::const_iterator end)
{
    vector<double> res = {0,0,0};
    size_t count = 0;
    for (DataFrame::const_iterator it = beg; it != end; ++it) {
        if ((*it).back() == 0) {
            res[0] += 1;
        } else if ((*it).back() == 1) {
            res[1] += 1;
        } else {
            res[2] += 1;
        }
        ++count;
    }
    transform(res.begin(), res.end(), res.begin(), [count](int &c){ return c/count; });
    return res;
}

double calc_entropy(const vector<double> &freqs)
{
    double entropy = 0;
    for (vector<double>::const_iterator it = freqs.cbegin(); it != freqs.cend(); ++it) {
        if (*it == 0) {
            continue;
        }
        entropy -= *it * log2(*it);
    }
    return entropy;
}

double calc_split_info(const vector<double> &freqs)
{
    double split_info = 0;
    double total_labels = 0;
    for (vector<double>::const_iterator it = freqs.cbegin(); it != freqs.cend(); ++it) {
        total_labels += *it;
    }
    for (vector<double>::const_iterator it = freqs.cbegin(); it != freqs.cend(); ++it) {
        split_info -= (*it / total_labels) * log2(*it / total_labels);
    }
}

vector<double> get_best_split(DataFrame &df)
{
    vector<double> best_split = {0,0};
    vector<double> left_freqs;
    vector<double> right_freqs;
    double information_gain_ratio = 0; 
    for (size_t feature = 0; feature != df[0].size() - 2; ++feature) {
        sort(df.begin(), df.end(), [feature] (const vector<double> &a, const vector<double> &b) { return a[feature] < b[feature]; });
        for (size_t value = 0; value != df.size() - 2; ++value) {
            if ((value != 0 && df[feature][value] == df[feature][value - 1]) || df[feature][value] == df[feature][value + 1]) {
                continue;    
            }
            left_freqs = get_label_frequencies(df.cbegin(), df.cbegin() + value + 1);
            right_freqs = get_label_frequencies(df.cbegin() + value, df.cend());
            
        }
    }
        
}