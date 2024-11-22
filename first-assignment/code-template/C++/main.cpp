#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>

unsigned int n_Hauler = 1;
unsigned int n_LP = 0;
unsigned int n_ULP = 0;
unsigned int n_SO = 0;
unsigned int n_CS = 1;
std::vector<std::pair<unsigned int, unsigned int>> init_haulers;
std::vector<std::pair<unsigned int, unsigned int>> LP_positions;
std::vector<std::pair<unsigned int, unsigned int>> ULP_positions;
std::vector<std::pair<unsigned int, unsigned int>> SO_positions;
std::vector<std::pair<unsigned int, unsigned int>> CS_positions;
unsigned int batery_capacity = 0;
unsigned int initial_energy = 0;

std::vector<std::vector<std::string>> mission;

void read_config(std::string fileName = "config.txt")
{
    std::ifstream file(fileName);
    std::string line;

    // variable to keep track of file line
    std::size_t index = 1;
    while (getline(file, line))
    {
        // read number of Haulers
        if (index == 1)
        {
            n_Hauler = std::stoi(line.substr(0, line.find("\t//")));
        }
        // read number of LPs
        else if (index == 2)
        {
            n_LP = std::stoi(line.substr(0, line.find("\t//")));
        }
        // read number of ULPs
        else if (index == 3)
        {
            n_ULP = std::stoi(line.substr(0, line.find("\t//")));
        }
        // read number of SOs
        else if (index == 4)
        {
            n_SO = std::stoi(line.substr(0, line.find("\t//")));
        }
        // read number of CSs
        else if (index == 5)
        {
            n_CS = std::stoi(line.substr(0, line.find("\t//")));
        }
        // read Initial position of haulers
        else if (index == 6)
        {
            std::string temp = line.substr(0, line.find("\t//"));
            std::size_t pos = 0;
            std::string token;
            std::string delimiter = "-";
            unsigned int x, y;
            while ((pos = temp.find(delimiter)) != std::string::npos)
            {
                token = temp.substr(0, pos);
                sscanf(token.c_str(), "[%d,%d]", &x, &y);
                init_haulers.push_back(std::make_pair(x, y));
                temp.erase(0, pos + delimiter.length());
            }
            sscanf(temp.c_str(), "[%d,%d]", &x, &y);
            init_haulers.push_back(std::make_pair(x, y));
        }

        // read position of LPs
        else if (index == 7)
        {
            std::string temp = line.substr(0, line.find("\t//"));
            std::size_t pos = 0;
            std::string token;
            std::string delimiter = "-";
            unsigned int x, y;
            while ((pos = temp.find(delimiter)) != std::string::npos)
            {
                token = temp.substr(0, pos);
                sscanf(token.c_str(), "[%d,%d]", &x, &y);
                LP_positions.push_back(std::make_pair(x, y));
                temp.erase(0, pos + delimiter.length());
            }
            sscanf(temp.c_str(), "[%d,%d]", &x, &y);
            LP_positions.push_back(std::make_pair(x, y));
        }

        // read position of ULPs
        else if (index == 8)
        {
            std::string temp = line.substr(0, line.find("\t//"));
            std::size_t pos = 0;
            std::string token;
            std::string delimiter = "-";
            unsigned int x, y;
            while ((pos = temp.find(delimiter)) != std::string::npos)
            {
                token = temp.substr(0, pos);
                sscanf(token.c_str(), "[%d,%d]", &x, &y);
                ULP_positions.push_back(std::make_pair(x, y));
                temp.erase(0, pos + delimiter.length());
            }
            sscanf(temp.c_str(), "[%d,%d]", &x, &y);
            ULP_positions.push_back(std::make_pair(x, y));
        }

        // read position of SOs
        else if (index == 9)
        {
            if (n_SO != 0)
            {
                std::string temp = line.substr(0, line.find("\t//"));
                std::size_t pos = 0;
                std::string token;
                std::string delimiter = "-";
                unsigned int x, y;
                while ((pos = temp.find(delimiter)) != std::string::npos)
                {
                    token = temp.substr(0, pos);
                    sscanf(token.c_str(), "[%d,%d]", &x, &y);
                    SO_positions.push_back(std::make_pair(x, y));
                    temp.erase(0, pos + delimiter.length());
                }
                sscanf(temp.c_str(), "[%d,%d]", &x, &y);
                SO_positions.push_back(std::make_pair(x, y));
            }
        }

        // read position of CSs
        else if (index == 10)
        {
            if (n_CS != 0)
            {
                std::string temp = line.substr(0, line.find("\t//"));
                std::size_t pos = 0;
                std::string token;
                std::string delimiter = "-";
                unsigned int x, y;
                while ((pos = temp.find(delimiter)) != std::string::npos)
                {
                    token = temp.substr(0, pos);
                    sscanf(token.c_str(), "[%d,%d]", &x, &y);
                    CS_positions.push_back(std::make_pair(x, y));
                    temp.erase(0, pos + delimiter.length());
                }
                sscanf(temp.c_str(), "[%d,%d]", &x, &y);
                CS_positions.push_back(std::make_pair(x, y));
            }
        }

        // read battery capacity
        if (index == 11)
        {
            if (n_CS != 0)
                batery_capacity = std::stoi(line.substr(0, line.find("\t//")));
        }

        // read initial energy
        if (index == 12)
        {
            if (n_CS != 0)
                initial_energy = std::stoi(line.substr(0, line.find("\t//")));
        }

        index++;
    }

    file.close();
}

void read_mission(std::string fileName = "mission.txt")
{
    std::ifstream file(fileName);
    std::string line;
    while (getline(file, line))
    {
        std::string temp = line.substr(0, line.find("\t//"));
        std::size_t pos = 0;
        std::string token;
        std::string delimiter = ",";
        std::vector<std::string> mission_temp;
        while ((pos = temp.find(delimiter)) != std::string::npos)
        {
            token = temp.substr(0, pos);
            mission_temp.push_back(token);
            temp.erase(0, pos + delimiter.length());
        }
        mission_temp.push_back(temp);
        mission.push_back(mission_temp);
    }
}

void write_output(unsigned int makespan, std::vector<unsigned int> completion_times, int64_t elapsed_time, std::string path, std::string fileName = "output.txt")
{
    std::ofstream file;
    file.open(fileName);
    file << ("//Quantitative values\n");
    file << std::to_string(makespan) << "\t//Makespan" << "\n";

    for (size_t i = 0; i < completion_times.size(); i++)
    {
        file << completion_times[i]<< "\t//Mission completion time hauler " << std::to_string(i + 1)  << "\n";
    }

    file << std::to_string(elapsed_time) << "\t//Application execution time (in millisecond)" << "\n";
    file << "//Path to the final points\n";
    file << path;
    file.close();
}

int main()
{
    /*
    Replace your input files location and name.
    You can also use command line argument to get input files name.

    functions:
        read_config     -> input: config file name
                        -> output: all variables in config file
                        NOTICE: the cordinates defined as a std::pair (look at the bellow example)
                        example:
                            if you want the x position of second LP:
                                 LP_positions[1].first
                            similarly, if you want the y position of second LP:
                                 LP_positions[1].second



        read_mission    -> input: mission file name
                        -> output: mission for each hauler
                        example:
                            if you want second goal of second hauler:
                                mission[1][1]
                                
        
        write_output    -> input: scenario makespan, completion time of each hauler, elapsed time of program,
                                     path to the final points, output file name
                        -> output: void
    */
    std::string config_file = "config.txt";
    std::string mission_file = "mission.txt";
    std::string output_file = "output.txt";
    read_config(config_file);
    read_mission(mission_file);

    auto tstart = std::chrono::high_resolution_clock::now();
    // ------------------------
    // Place your code here!


    // ------------------------
    auto tend = std::chrono::high_resolution_clock::now();
    auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(tend - tstart).count();

    // call the writing function here
    // example:
    // std::vector<unsigned int> completion_times{10, 15};
    // write_output(200, completion_times, elapsed_time, "1,[11,9],[8,12],[7,11]\n2,[11,8],[8,11],[7.10]");

    return 0;
}