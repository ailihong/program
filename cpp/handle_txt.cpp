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

ifstream fid_video_list;//input 
fid_video_list.open(video_list);
string line;
if(fid_video_list.is_open()){
	while (!fid_video_list.eof()) {
		fid_video_list >> line;//without \n
		cout << "reading...... " << line << endl;
        ...
fid_image_list.close();
        
ofstream fid_error_result("predict_error_list.txt");
fid_error_result << line.substr(line.rfind('/') + 1, line.length())
                               << "--svm_predict->" << result[int((response_svm + 1) / 2)] << endl;
fid_error_result.close()
