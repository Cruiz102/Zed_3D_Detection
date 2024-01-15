#include <random>
#include <iostream>
#include <fstream>
#include <chrono>
// # include "logger.hpp"
double readFile(const std::string& filePath, int chunkSize, int numReads) {
    std::ifstream file(filePath, std::ifstream::binary);
    if (!file) {
        std::cerr << "Error opening file: " << filePath << std::endl;
        return -1;
    }

    // Get the size of the file
    file.seekg(0, file.end);
    int fileSize = file.tellg();
    file.seekg(0, file.beg);

    // Create a buffer for reading
    char* buffer = new char[chunkSize];

    // Random number generation
    std::mt19937 gen; // Standard mersenne_twister_engine
    std::uniform_int_distribution<> distrib(0, fileSize - chunkSize);

    auto start = std::chrono::high_resolution_clock::now();

    // Perform random reads
    for (int i = 0; i < numReads; ++i) {
        int randomPosition = distrib(gen);
        file.seekg(randomPosition);
        file.read(buffer, chunkSize);
    }

    auto end = std::chrono::high_resolution_clock::now();

    delete[] buffer;

    std::chrono::duration<double, std::milli> elapsed = end - start;
    return elapsed.count(); // Time in milliseconds
}



int main(int argc, char** argv) {



        int a = readFile("/media/cesarruiz/UBUNTU 22_0/testData.txt", 10, 5000000);
        std::cout << "Time taken: " << a << " ms" << std::endl;

        // createWeights();


        // randomReadBenchmark();


        // sequientialReadBenchmark();


        // randomWriteBenchmark();


        // sequientialWriteBenchmark();



        // Logger logger = Logger("Logger");






        return 0;
    }