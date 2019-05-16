#include "myDataBase.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <error.h>

int gBinFd;
char gDbFileName[FILENAME_LENGTH];
int writeNumRecords(int *pFd, int num){
    int ret = 0,rval;
    do{ 
        if(*pFd < 0){
            printf("bin file is in error\n");
            ret = -1;
            break;
        }
        lseek(*pFd,0,SEEK_SET);//start+0
        rval = write(*pFd,&num,BTYES_NUM_RECOEDS);
        if(rval != BTYES_NUM_RECOEDS){
            printf("write file error\n");
            ret = -1;
            break;
        }
    }while(0);
	
	return ret;
}
int readNumRecords(int *pFd, int *pnum){
    int ret = 0,rval;
    do{ 
        if(*pFd < 0){
            printf("bin file is in error\n");
            ret = -1;
            break;
        }
        ret = lseek(*pFd,0,SEEK_SET);//start+0
        rval = read(*pFd,pnum,BTYES_NUM_RECOEDS);
        if(rval != BTYES_NUM_RECOEDS){
            printf("read file size error,%d == %d\n",BTYES_NUM_RECOEDS,rval);
            ret = -1;
            break;
        }
    }while(0);
	
	return ret;
}
long get_file_size(const char *path){
	struct stat statbuff;

	if (stat(path, &statbuff) < 0) {
		return -1;
	} else {
		return statbuff.st_size;
	}
}
int openBinFile(char *fname, int *pFd) {

    int ret = 0,rval;
    int numRecode=0;
    do{
        //file is exists
        if(get_file_size(fname) != -1){
            numRecode=-1;
        }
        *pFd = open(fname,O_RDWR|O_CREAT);
        if(*pFd < 0){
            printf("open file error\n");
            ret = -1;
            break;
        }
        
        if(numRecode < 0)break;
        rval = write(*pFd,&numRecode,BTYES_NUM_RECOEDS);
        if(rval != BTYES_NUM_RECOEDS){
            printf("write file error\n");
            ret = -1;
            break;
        }
    }while(0);
    
	return ret;
}
int openBinFile_global(char *fname){
    int ret = 0;
    ret = openBinFile(fname,&gBinFd);
    strncpy(gDbFileName, fname, FILENAME_LENGTH);//must do once before deleteRecord
    return ret;
}
int addBinFile(record record_a) {
	int ret = 0,rval;
    int numRecode=0,offSetRecords=0;
    do{ 
        if(gBinFd < 0){
            printf("bin file is in error\n");
            ret = -1;
            break;
        }
        readNumRecords(&gBinFd, &numRecode);
        offSetRecords = BTYES_NUM_RECOEDS+numRecode*BTYES_A_RECOEDS;
        lseek(gBinFd,offSetRecords,SEEK_SET);//start+
        rval = write(gBinFd,&record_a,BTYES_A_RECOEDS);
        if(rval != BTYES_A_RECOEDS){
            printf("write file error,%d == %d\n",BTYES_A_RECOEDS,rval);
            ret = -1;
            break;
        }
        numRecode++;
        writeNumRecords(&gBinFd, numRecode);
    }while(0);
	
	return ret;
}
//ret = 1,means find it
int findBinFile(record * precord) {
    int ret = 0;
    record record_a;
    int numRecode=0,offSetRecords=0,i,rval;
	do{
        if(!precord){
            ret = -1;
            printf("addr is no mem!");
            break;
        }
        readNumRecords(&gBinFd, &numRecode);
        lseek(gBinFd,BTYES_NUM_RECOEDS,SEEK_SET);//start+
        for(i=0;i<numRecode;i++){
            rval = read(gBinFd,&record_a,BTYES_A_RECOEDS);
            if(rval != BTYES_A_RECOEDS){
                printf("read file error\n");
                ret = -1;
                break;
            }
            if(strcmp(precord->name,record_a.name)==0){//find it
                //*precord = record_a;
                memcpy(precord,&record_a,sizeof(record));
                ret = 1;
                break;
            }
        }
        
    }while(0);
	
	return ret;
}
int deleteRecordByName(char *searchname) {
	
	int idx=-1,ret=0,i,j;
	record record_a;
    int DBFd,numRecode=0,offSetRecords=0,rval;
	
	readNumRecords(&gBinFd, &numRecode);
	do{

        lseek(gBinFd,BTYES_NUM_RECOEDS,SEEK_SET);//start+
        for(i=0,j=0;i<numRecode;i++){
            rval = read(gBinFd,&record_a,BTYES_A_RECOEDS);
            if(rval != BTYES_A_RECOEDS){
                printf("read file error\n");
                ret = -1;
                break;
            }
            if(strcmp(searchname,record_a.name)==0){//find it
                idx=i;
                break;
            }
        }
        if(idx == -1){
            ret = 0;
            printf("No record(s) found with the requested name: %s\n\n", searchname);
            break;
        }
        openBinFile("temp_db.bin", &DBFd);

        lseek(gBinFd,BTYES_NUM_RECOEDS,SEEK_SET);//start+
        for(i=0,j=0;i<numRecode;i++){
            if(i == idx)continue;
            rval = read(gBinFd,&record_a,BTYES_A_RECOEDS);
            if(rval != BTYES_A_RECOEDS){
                printf("read file error\n");
                ret = -1;
                break;
            }
            offSetRecords = BTYES_NUM_RECOEDS+j*BTYES_A_RECOEDS;
            lseek(DBFd,offSetRecords,SEEK_SET);//start+
            rval = write(DBFd,&record_a,BTYES_A_RECOEDS);
            if(rval != BTYES_A_RECOEDS){
                printf("write file error\n");
                ret = -1;
                break;
            }
            j++;
        }

        close(gBinFd);
        close(DBFd);
        remove(gDbFileName);
	    rename("temp_db.bin", gDbFileName);
        openBinFile(gDbFileName, &gBinFd);//reopen
    }while(0);

	return ret;
}
int updateRecord(record  record_){
    int ret = 0;
    record record_a;
    int numRecode=0,offSetRecords=0,i,rval,idx=-1;
	do{
        //find
        readNumRecords(&gBinFd, &numRecode);
        lseek(gBinFd,BTYES_NUM_RECOEDS,SEEK_SET);//start+
        for(i=0;i<numRecode;i++){
            rval = read(gBinFd,&record_a,BTYES_A_RECOEDS);
            if(rval != BTYES_A_RECOEDS){
                printf("read file error\n");
                ret = -1;
                break;
            }
            if(strcmp(record_.name,record_a.name)==0){//find it
                idx = i;
                break;
            }
        }

        //update
        offSetRecords = BTYES_NUM_RECOEDS+idx*BTYES_A_RECOEDS;
        lseek(gBinFd,offSetRecords,SEEK_SET);//start+
        rval = write(gBinFd,&record_,BTYES_A_RECOEDS);
        if(rval != BTYES_A_RECOEDS){
            printf("write file error\n");
            ret = -1;
            break;
        }
        
    }while(0);
	
	return ret;
}
