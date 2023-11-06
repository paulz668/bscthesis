#ifndef NODE_HPP
#define NODE_HPP

#include <vector>

using namespace std;
using DataFrame = vector<vector<double>>;

class Node{

    public:
        // default contructor
        Node() = default;
        // root node constructor
        Node(DataFrame &df): data(df), parent(nullptr), left(nullptr), 
                                right(nullptr), entropy(calc_entropy(get_label_frequencies(df))) {}
        // non-root node constructor
        Node(DataFrame &df, Node *p, double e): data(df), parent(p), left(nullptr), 
                                right(nullptr), entropy(e) {}

        // getter methods
        Node *get_parent() { return this->parent; }
        Node *get_left() { return this->left; }
        Node *get_right() { return this->right; }

        DataFrame &get_data() { return this->data; }

        double &get_entropy() { return this->entropy; }
        vector<double> &get_best_split() { return this->best_split; }

        // setter methods
        void set_parent(Node *p) { this->parent = p; }
        void set_left(Node *l) { this->left = l; }
        void set_right(Node *r) { this->right = r; }

        void set_entropy(double e) { this->entropy = e; }
        void set_best_split(vector<double> bS) { this->best_split = bS; }

    private:
        Node *parent;
        Node *left;
        Node *right;

        // training data
        DataFrame &data;

        // entropy before split
        double entropy;
        // feature and value to split on
        vector<double> best_split = {0,0};
};

vector<double> get_label_frequencies(const DataFrame &df);
vector<double> get_label_frequencies(DataFrame::const_iterator beg, DataFrame::const_iterator end);
double calc_entropy(const vector<double> &freqs);
vector<double> calc_best_split(Node &);

#endif