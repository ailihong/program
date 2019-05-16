#include "myDataBase.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc,char ** argv){
    char mydb[FILENAME_LENGTH]="test.db";
    int find=0;
    //open
    openBinFile_global(mydb);
    
    record record_a={.name="aaa",
                    .feature={1.0,2.0,0.0}};

    record record_b={.name="bbb",
                    .feature={2.0,2.0,0.0}};
    //insert
    addBinFile(record_a);
    addBinFile(record_b);
    
    //find
    memset(&record_a,0,sizeof(record_a));
    strncpy(record_a.name,"aaa",sizeof("aaa"));
    printf("%s\n",record_a.name);
    findBinFile(&record_a);
    printf("%f %f\n",record_a.feature[0],record_a.feature[1]);
    //update
    record_a.feature[2]=2.5;
    updateRecord(record_a);
    memset(record_a.feature,0,sizeof(record_a.feature));
    find = findBinFile(&record_a);
    printf("find:%d\n",find);
    printf("%f %f\n",record_a.feature[0],record_a.feature[2]);
    //delete
    deleteRecordByName(record_b.name);
    find = findBinFile(&record_b);
    printf("find:%d\n",find);
    return 0;
}
