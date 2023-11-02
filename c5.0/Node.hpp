#ifndef NODE_HPP
#define NODE_HPP

#include <vector>

using DataFrame vector<vector<int>>;

class Node{

    public:
        // default contructor
        Node() = default;
        // root node constructor
        Node(const DataFrame &df): data(df), parent(nullptr), left(nullptr), 
                                right(nullptr), entropy(calc_entropy(df)), feature(calc_feature(df)),
                                value(calc_value(df)) {}
        // non-root node constructor
        Node(const DataFrame &df, Node *p, double e): data(df), parent(p), left(nullptr), 
                                right(nullptr), entropy(e), feature(calc_feature(df)), 
                                value(calc_value(df)) {}

        // getter methods
        Node *get_parent() { return this->parent; }
        Node *get_left() { return this->left; }
        Node *get_right() { return this->right; }

        DataFrame &get_data() { return this->data; }

        double &get_entropy() { return this->entropy; }
        int &get_feature() { return this->feature; }
        double &get_value() { return this->value; }

        // setter methods
        void set_parent(Node *p) { this->parent = p; }
        void set_left(Node *l) { this->left = l; }
        void set_right(Node *r) { this->right = r; }

        void set_entropy(double e) { this->entropy = e; }
        void set_feature(int f) { this->feature = f; }
        void set_value(double v) { this->value = v;}

    private:
        Node *parent;
        Node *left;
        Node *right;

        // training data
        DataFrame &data;

        // entropy before split
        double entropy;
        // feature to split on
        int feature;
        // value to split on
        double value;
};

double calc_entropy(DataFrame &);
int calc_feature(DataFrame &);
double calc_value(DataFrame &);

#endif