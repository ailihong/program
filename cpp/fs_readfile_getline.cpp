#include <fstream>  // NOLINT(readability/streams)
#include <string>
#include <vector>
#include <iostream>
using namespace std;

int main(int argc, char** argv){
    if(argc < 2){
    cout << "enter param" << endl;
    }
    std::ifstream f1(argv[1], std::ios::in);
    vector<string>words;
    string      line1;
    while(getline(f1,line1))//without \n
    {
        words.push_back(line1);  
    }
    for(int i=0;i<words.size();i++)
    cout << words[i]<< endl;
    return 0;
}
