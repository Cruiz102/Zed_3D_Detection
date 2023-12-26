// main.cpp
#include <iostream>
#include "cudaFunctions.cuh"

int main() {
    const int n = 1024;
    float h_output[n];

    // Call the function to run the kernel
    runBackProject2Dto3D(h_output, n);

    // Print the results
    for (int i = 0; i < n; ++i) {
        std::cout << "Output[" << i << "] = " << h_output[i] << std::endl;
    }

    return 0;
}
