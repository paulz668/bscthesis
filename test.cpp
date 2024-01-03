#include <iostream>
#include <vector>

std::vector<double> sumVectors(const std::vector<std::vector<double>>& df) {
    // Check if df is not empty
    if (df.empty() || df[0].empty()) {
        std::cerr << "Error: Empty vector or inner vectors in df." << std::endl;
        return {};  // Return an empty vector indicating an error
    }

    // Get the length of the inner vectors (assuming all inner vectors have the same length)
    size_t n = df[0].size();

    // Create a vector to store the sum of elements
    std::vector<double> sumVector(n, 0.0);

    // Loop through each inner vector and add its elements to the sumVector
    for (const auto& innerVec : df) {
        // Check if the inner vector has the expected length
        if (innerVec.size() != n) {
            std::cerr << "Error: Inner vectors in df have different lengths." << std::endl;
            return {};  // Return an empty vector indicating an error
        }

        // Add the elements of the inner vector to the sumVector
        for (size_t i = 0; i < n; ++i) {
            sumVector[i] += innerVec[i];
        }
    }

    return sumVector;  // Return the sumVector
}

int main() {
    // Example usage:
    std::vector<std::vector<double>> df = {{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}, {7.0, 8.0, 9.0}};

    // Call the sumVectors function
    std::vector<double> result = sumVectors(df);

    // Print the result
    for (double value : result) {
        std::cout << value << " ";
    }
    std::cout << std::endl;

    return 0;
}
