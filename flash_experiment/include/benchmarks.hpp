class Benchmark{


    public:

    Benchmark(std::string name);

    void randomReadBenchmark();
    void randomWriteBenchmark();
    void sequentialReadBenchmark();
    void sequentialWriteBenchmark();


    void writeResults2CSV(std::string filePath, std::vector<std::vector<double>> data);
}