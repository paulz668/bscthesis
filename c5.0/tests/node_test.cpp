#include "src/lib/Node.hpp"
#include <gtest/gtest.h>

// Test functionality of the helper function used in construction of Node object
TEST(NodeTest, HelperFunctionality) {

    DataFrame test_df = {
    {0, 0, 1, 1, 2}, // observation 1
    {0, 2, 2, 2, 1}, // observation 2
    {1, 1, 2, 0, 1}, // observation 3
    {2, 0, 0, 0, 0}, // observation 4
    {1, 1, 2, 1, 0}  // observation 5
    };

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

// Test basic functionality of Node class
TEST(NodeTest, BasicFunctionality) {
    EXPECT_TRUE(true);
}