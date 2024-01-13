class InputOutputOp{

    private:
    std::string name;


    public:
    InputOutputOp(std::string name);

    // double readFile();

    void read(std::string filePath, int chunkSize, int numReads);

    void write(std::string filePath, int chunkSize, int numWrites);

    void log(std::string message);

    




}