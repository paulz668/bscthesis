#include "src/lib/Node.hpp"
#include <gtest/gtest.h>

DataFrame test_df = {
{0, 0, 1, 1, 2}, // observation 1
{0, 2, 2, 2, 1}, // observation 2
{1, 1, 2, 0, 1}, // observation 3
{2, 0, 0, 0, 0}, // observation 4
{1, 1, 2, 1, 0}  // observation 5
};

// Test functionality of the helper function used in construction of Node object
TEST(NodeTest, HelperFunctionality) {

    vector<double> test_freqs1 = get_label_frequencies(test_df);
    vector<double> test_freqs2 = get_label_frequencies(test_df.cbegin(), test_df.cend());
    vector<double> test_freqs3 = get_label_frequencies(test_df.cbegin() + 1, test_df.cbegin() + 3);

    EXPECT_DOUBLE_EQ(test_freqs1[0], 0.4);
    EXPECT_DOUBLE_EQ(test_freqs1[1], 0.4);
    EXPECT_DOUBLE_EQ(test_freqs1[2], 0.2);

    EXPECT_DOUBLE_EQ(test_freqs2[0], 0.4);
    EXPECT_DOUBLE_EQ(test_freqs2[1], 0.4);
    EXPECT_DOUBLE_EQ(test_freqs2[2], 0.2);

    EXPECT_DOUBLE_EQ(test_freqs3[0], 0.0);
    EXPECT_DOUBLE_EQ(test_freqs3[1], 1.0);
    EXPECT_DOUBLE_EQ(test_freqs3[2], 0.0);

    EXPECT_DOUBLE_EQ(calc_entropy(test_freqs1), 1.5219280948873621);
    EXPECT_DOUBLE_EQ(calc_entropy(test_freqs3), 0.0);

}

double default_entropy = 0.0;
vector<double> default_best_split = {0.0, 0.0};

// Test basic functionality of Node class including getters and setters
TEST(NodeTest, BasicFunctionality) {
    
    Node test_node1();
    Node test_node2(test_df);
    Node *test_node_pointer2 = &test_node2;
    Node test_node3(test_df, test_node_pointer2, 1.5219280948873621);
    Node *test_node_pointer3 = &test_node3;

    EXPECT_EQ(test_node1.get_parent(), nullptr);
    EXPECT_EQ(test_node1.get_right(), nullptr);
    EXPECT_EQ(test_node1.get_left(), nullptr);
    EXPECT_EQ(test_node1.get_entropy(), default_entropy);
    EXPECT_EQ(test_node1.get_best_split(), default_best_split);
    
    test_node2.set_left(test_node_pointer3);

    EXPECT_EQ(test_node2.get_left(), test_node3);
    EXPECT_EQ(test_node3.get_parent(), test_node2);
    EXPECT_EQ(test_node3.get_data(), test_df);



}