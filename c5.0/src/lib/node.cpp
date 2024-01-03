#include "Node.hpp"

using namespace std;


vector<double> sumVectors(const vector<vector<double>>& df) {
    // Check if df is not empty
    if (df.empty() || df[0].empty()) {
        cerr << "Error: Empty vector or inner vectors in df." << endl;
        return {};  // Return an empty vector indicating an error
    }

    // Get the length of the inner vectors (assuming all inner vectors have the same length)
    size_t n = df[0].size();

    // Create a vector to store the sum of elements
    vector<double> sumVector(n, 0.0);

    // Loop through each inner vector and add its elements to the sumVector
    for (const auto& innerVec : df) {
        // Check if the inner vector has the expected length
        if (innerVec.size() != n) {
            cerr << "Error: Inner vectors in df have different lengths." << endl;
            return {};  // Return an empty vector indicating an error
        }

        // Add the elements of the inner vector to the sumVector
        for (size_t i = 0; i < n; ++i) {
            sumVector[i] += innerVec[i];
        }
    }

    return sumVector;  // Return the sumVector
}


vector<double> subtractVectors(const vector<double>& vec1, const vector<double>& vec2) {
    // Check if the input vectors are of the same size
    if (vec1.size() != vec2.size()) {
        cerr << "Error: Vectors must be of the same size for element-wise subtraction." << endl;
        return vector<double>();
    }

    // Create a vector to store the result
    vector<double> result;

    // Subtract elements element-wise
    for (size_t i = 0; i < vec1.size(); ++i) {
        result.push_back(vec1[i] - vec2[i]);
    }

    return result;
}

// return a vector of 2^depth quantiles of the DataFrame input based on the specified feature
// origin keeps track of the begining of the original DataFrame as this function recursively partitiones the input
vector<tuple<ptrdiff_t, double>> quantiling(DataFrame::iterator origin, DataFrame::iterator begin, DataFrame::iterator end, 
                          int depth, int feature)
{
    vector<tuple<ptrdiff_t, double>> res;
    DataFrame::size_type median = (end - begin) / 2;
    nth_element(begin, begin + median, end,
    [feature](const vector<double> &a, const vector<double> &b){
        return a[feature] < b[feature];
    });
    tuple<ptrdiff_t, double> res_tup = make_tuple(begin + median - origin, (*(begin + median))[feature]);
    res.push_back(res_tup);

    if (depth == 1) {
        return res;
    }

    vector<tuple<ptrdiff_t, double>> temp_l = quantiling(origin, begin, begin + median, depth - 1, feature);
    temp_l.insert(temp_l.end(), res.begin(), res.end());
    vector<tuple<ptrdiff_t, double>> temp_r = quantiling(origin, begin + median, end, depth - 1, feature);
    temp_l.insert(temp_l.end(), temp_r.begin(), temp_r.end());

    return temp_l;
}


// calculate the relative label frequencies in the data using start and end iterators
vector<double> get_label_frequencies(DataFrame::const_iterator beg, DataFrame::const_iterator end)
{
    vector<double> res = {0,0,0};
    for (DataFrame::const_iterator it = beg; it != end; ++it) {
        if ((*it).back() == 0) {
            res[0] += 1;
        } else if ((*it).back() == 1) {
            res[1] += 1;
        } else {
            res[2] += 1;
        }
    }
    return res;
}


// calculate the label frequencies for every quantile (histogram bin)
DataFrame &histogram(const DataFrame &df, const vector<tuple<ptrdiff_t, double>> &quantiles)
{
    DataFrame res;
    for (vector<tuple<ptrdiff_t, double>>::const_iterator i = quantiles.cbegin(); i != quantiles.cend(); ++i) {
        if (i == quantiles.cbegin()) {
            vector<double> temp = get_label_frequencies(df.cbegin(), df.cbegin() + get<0>(*i));
            res.push_back(temp);
            continue;
        }

        vector<double> temp = get_label_frequencies(df.cbegin() + get<0>(*(i-1)), df.cbegin() + get<0>(*i));
        res.push_back(temp);

        if ((i+1) == quantiles.cend()) {
            vector<double> temp = get_label_frequencies(df.cbegin() + get<0>(*i), df.cend());
            res.push_back(temp);
        }
    }
}


// calculate the gini index for the given label frequencies
double gini(const vector<double> &freqs)
{
    double gini = 1;
    double total = accumulate(freqs.cbegin(), freqs.cend(), 0);
    for (vector<double>::const_iterator i = freqs.cbegin(); i != freqs.cend(); ++i) {
        gini -= pow(*i, 2);
    }
    return gini;
}


// calculate the gini index after a split given the label frequencies of both datasubsets
double gini_as(const vector<double> &freqs1, const vector<double> &freqs2)
{
    double subtotal1 = accumulate(freqs1.cbegin(), freqs1.cend(), 0);
    double subtotal2 = accumulate(freqs2.cbegin(), freqs2.cend(), 0);
    double total = subtotal1 + subtotal2;
    return subtotal1 / total * gini(freqs1) + subtotal2 / total * gini(freqs2);
}


// estimating the minimum gini index from left to right
double gini_est_lr(vector<double> &first, const vector<double> &second, const vector<double> &total)
{
    // initialize variables
    double min_gradient;
    double temp_gradient;
    double min_index;
    double gini_est;
    double total_obs = accumulate(total.cbegin(), total.cend(), 0);
    double obs_less = accumulate(first.cbegin(), first.cend(), 0);

    // check if the first interval is zero
    bool zerosF = all_of(first.cbegin(), first.cend(), [](int i) { return i==0; });
    // check if the second interval is equal to total
    bool equalTS = second == total;

    // special case if the first interval is zero
    if (zerosF) {
        vector<double>::const_iterator minimum = min_element(second.cbegin(), second.cend());
        min_gradient = *minimum;
        min_index = minimum - second.cbegin();    
        first[min_index] = min_gradient;   
        gini_est = gini_as(first, subtractVectors(total, first));
        return gini_est;
    }

    for (vector<double>::const_iterator i = total.cbegin(); i != total.cend(); ++i) {
        if (i == total.cbegin()) {
            min_gradient = *i * (obs_less / total_obs) - first[0];
            min_index = 0;
            continue;
        }
        temp_gradient = *i * (obs_less / total_obs) - first[i - total.cbegin()];
        if (temp_gradient < min_gradient) {
            min_gradient = temp_gradient;
            min_index = i - total.cbegin();
        }
    }
    first[min_index] = second[min_index];   
    gini_est = gini_as(first, subtractVectors(total, first));
    return gini_est;
}



// estimating the minimum gini index from left to right
double gini_est_rl(vector<double> &first, const vector<double> &second, const vector<double> &total)
{
    // initialize variables
    double max_gradient;
    double temp_gradient;
    double max_index;
    double gini_est;
    double total_obs = accumulate(total.cbegin(), total.cend(), 0);
    double obs_less = accumulate(first.cbegin(), first.cend(), 0);

    // check if the first interval is zero
    bool zerosF = all_of(first.cbegin(), first.cend(), [](int i) { return i==0; });
    // check if the second interval is equal to total
    bool equalTS = second == total;

    // special case if the first interval is zero
    if (zerosF) {
        vector<double>::const_iterator maximum = max_element(second.cbegin(), second.cend());
        max_gradient = *maximum;
        max_index = maximum - second.cbegin();    
        first[max_index] = max_gradient;   
        gini_est = gini_as(first, subtractVectors(total, first));
        return gini_est;
    }

    for (vector<double>::const_iterator i = total.cbegin(); i != total.cend(); ++i) {
        if (i == total.cbegin()) {
            max_gradient = *i * (obs_less / total_obs) - first[0];
            max_index = 0;
            continue;
        }
        temp_gradient = *i * (obs_less / total_obs) - first[i - total.cbegin()];
        if (temp_gradient < max_gradient) {
            max_gradient = temp_gradient;
            max_index = i - total.cbegin();
        }
    }
    first[max_index] = second[max_index];   
    gini_est = gini_as(first, subtractVectors(total, first));
    return gini_est;
}


// calculate entropy based on the relative frequencies of labels
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

// calculate the best split (feature and value) by maximising the information gain ratio of each candidate split
vector<double> calc_best_split(Node &node)
{
    DataFrame &df = node.get_data();
    vector<double> best_split = {0,0};
    vector<double> left_freqs, right_freqs;

    double left_info, right_info, average_info;
    double information_gain_ratio = 0, best_information_gain_ratio = 0;
    double f;

    for (size_t feature = 0; feature != df[0].size() - 2; ++feature) {
        sort(df.begin(), df.end(), [feature] (const vector<double> &a, const vector<double> &b) { return a[feature] < b[feature]; });
        for (size_t value = 0; value != df.size() - 2; ++value) {
            if ((value != 0 && df[feature][value] == df[feature][value - 1]) || df[feature][value] == df[feature][value + 1]) {
                continue;    
            }
            left_freqs = get_label_frequencies(df.cbegin(), df.cbegin() + value + 1);
            right_freqs = get_label_frequencies(df.cbegin() + value, df.cend());

            left_info = calc_entropy(left_freqs);
            right_info = calc_entropy(right_freqs);
            average_info = (left_info * (value + 1) + right_info * (df.size() - (value + 1))) / df.size();

            information_gain_ratio = (node.get_entropy() - average_info) / node.get_entropy(); 

            if (information_gain_ratio > best_information_gain_ratio) {
                best_information_gain_ratio = information_gain_ratio;
                f = feature; // the conversion of feature from unsigned int to double is accurate up to the 53rd power of 2, for an IEEE754 double precision floating point type
                best_split = {f, df[feature][value]};  
            }
        }
    }

    return best_split;
        
}