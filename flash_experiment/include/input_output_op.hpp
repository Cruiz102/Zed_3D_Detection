#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <sys/stat.h>
#include <sys/types.h>



namespace InputOutputOp {


    // Function to generate random binary data
    void generateRandomData(std::ofstream& file, int size) {
        for (int i = 0; i < size; ++i) {
            char randomByte = static_cast<char>(rand() % 256);
            file.write(&randomByte, sizeof(randomByte));
        }
    }



    // Function to create directories and files recursively
    void createRandomStructure(const std::string& baseDir, int depth, int maxDepth, int maxFiles, int fileSize) {
        if (depth > maxDepth) return;

        // Create a random number of directories in the current directory
        int numDirs = rand() % 5; // You can change 5 to any other number to control max directories
        for (int i = 0; i < numDirs; ++i) {
            std::string dirPath = baseDir + "/dir_" + std::to_string(i);
            mkdir(dirPath.c_str(), 0777);

            // Recursively create structure in the new directory
            createRandomStructure(dirPath, depth + 1, maxDepth, maxFiles, fileSize);
        }

        // Create a random number of files in the current directory
        int numFiles = rand() % maxFiles;
        for (int i = 0; i < numFiles; ++i) {
            std::string fileName = baseDir + "/file_" + std::to_string(i) + ".bin";
            std::ofstream file(fileName, std::ios::binary);
            if (file.is_open()) {
                generateRandomData(file, fileSize);
                file.close();
            } else {
                std::cerr << "Unable to open file: " << fileName << std::endl;
            }
        }
    }

    // Create a nested directory with random binary files
    //  for testing performance of random reads and writes
    void createRandomDirectory(const std::string& filePath, int numFiles, int seed, int fileSize) {
        srand(seed);
        for (int i = 0; i < numFiles; ++i) {
            std::string fileName = filePath + "/file_" + std::to_string(i) + ".bin";
            std::ofstream file(fileName, std::ios::binary);
            if (file.is_open()) {
                generateRandomData(file, fileSize);
                file.close();
            } else {
                std::cerr << "Unable to open file: " << fileName << std::endl;
            }
        }
    }




}