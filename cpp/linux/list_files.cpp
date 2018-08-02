//读取指定目录下的文件名
#include <dirent.h>
#include <stdio.h>
/*struct dirent
{
   long d_ino; // inode number 索引节点号
   off_t d_off; // offset to this dirent 在目录文件中的偏移
   unsigned short d_reclen; // length of this d_name 文件名长
   unsigned char d_type; // the type of d_name 文件类型
   char d_name [NAME_MAX+1]; // file name (null-terminated) 文件名，最长255字符
}
其中d_type表明该文件的类型：文件(8)、目录(4)、链接文件(10)等
*/
int main(){
    DIR *directory_pointer;
    struct dirent *entry;
    if((directory_pointer=opendir("/home/bai/dl/data/face4000_xingxun"))==NULL){
        printf("Error open\n");
        return -1;
    } else {
        while((entry=readdir(directory_pointer))!=NULL){
            if(entry->d_name[0]=='.') continue;
            printf("%s\n",entry->d_name);
        }
    }
    return 0;
}

//递归读取文件夹下所有文件
#include <iostream>
#include <string>
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
extern "C"{
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>
    #include <errno.h>
    #include <dirent.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
}
using namespace std;

void getAllFiles(string path, vector<string>& files)
{
    DIR *dir;
    struct dirent *ptr;
    if((dir=opendir(path.c_str()))==NULL){
        perror("Open dri error...");
        exit(1);
    }
    while((ptr=readdir(dir))!=NULL){
        if(strcmp(ptr->d_name,".")==0||strcmp(ptr->d_name,"..")==0)
            continue;
        else if(ptr->d_type==8)//file
            files.push_back(path+"/"+ptr->d_name);
        else if(ptr->d_type==10)//link file
            continue;
        else if(ptr->d_type==4){
            //files.push_back(ptr->d_name);//dir
            getAllFiles(path+"/"+ptr->d_name,files);
        }
    }
    closedir(dir);
}
int main(int argc,char **argv){
    if(argc<2){
        cout<<"USAGE:./a.out path"<<endl;
        exit(-1);
    }
    char * filePath = argv[1];
    vector<string> files;
    char * distAll = "allFiles.txt";
    getAllFiles(filePath, files);
    ofstream ofn(distAll);
    int size = files.size();
    //ofn << size << endl;
    for (int i = 0; i<size; i++)
    {
        ofn << files[i] << endl;
    }
    ofn.close();
    return 0;
}
