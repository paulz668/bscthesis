#ifndef NODE_HPP
#define NODE_HPP

#include <vector>
#include <algorithm>
#include <cmath>
#include <tuple>
#include <numeric>
#include <iostream>

using namespace std;
using DataFrame = vector<vector<double>>;

vector<tuple<ptrdiff_t, double>> quantiling(DataFrame::iterator, DataFrame::iterator, DataFrame::iterator, int, int);

vector<double> get_label_frequencies(DataFrame::const_iterator, DataFrame::const_iterator);

DataFrame &histogram(const DataFrame &, const vector<tuple<ptrdiff_t, double>> &);

double gini(const vector<double> &);
double gini_as(const vector<double> &, const vector<double> &);
double gini_est_lr(const DataFrame &);
double gini_est_rl(const DataFrame &);

class Node {

    public:
        // Define root node constructor
        Node(DataFrame &df): data(df), parent(nullptr), left(nullptr), 
                                right(nullptr), entropy(calc_entropy(get_label_frequencies(df))) {}
        // Define non-root node constructor
        Node(DataFrame &df, Node *p, double e): data(df), parent(p), left(nullptr), 
                                right(nullptr), entropy(e) {}

        // Define equality operator
        bool operator==(const Node &other) const {
        // Compare data, entropy, and best_split
            return (data == other.data) &&
                (entropy == other.entropy) &&
                (best_split == other.best_split);
        }

        // Define inequality operator
        bool operator!=(const Node &other) const {
            return !(*this == other);
        }

        // Define getter methods
        Node *get_parent() { return this->parent; }
        Node *get_left() { return this->left; }
        Node *get_right() { return this->right; }

        DataFrame &get_data() { return this->data; }

        double &get_entropy() { return this->entropy; }
        vector<double> &get_best_split() { return this->best_split; }

        // Define setter methods
        void set_parent(Node *p) { this->parent = p; }
        void set_left(Node *l) { this->left = l; }
        void set_right(Node *r) { this->right = r; }

        void set_entropy(double e) { this->entropy = e; }
        void set_best_split(vector<double> bS) { this->best_split = bS; }

    private:
        Node *parent;
        Node *left;
        Node *right;

        // Training data
        DataFrame &data;
        // Empty DataFrame for default initialization
        static DataFrame emptyDataFrame;

        // Entropy before split
        double entropy;
        // Feature and value to split on
        vector<double> best_split = {0.0, 0.0};
};

// Implement == and != for vector<double> and vector<vector<double>>
bool operator==(const vector<double> &a, const vector<double> &b) {
    return std::equal(a.begin(), a.end(), b.begin(), b.end());
}

bool operator!=(const vector<double> &a, const vector<double> &b) {
    return !(a == b);
}
 
bool operator==(const vector<vector<double>> &a, const vector<vector<double>> &b) {
    return std::equal(a.begin(), a.end(), b.begin(), b.end());
}

bool operator!=(const vector<vector<double>> &a, const vector<vector<double>> &b) {
    return !(a == b);
}

vector<double> calc_best_split(Node &);

#endif