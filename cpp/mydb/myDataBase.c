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
#define MAX_NUM_RECORD 50
query_simi ret_query_[MAX_NUM_RECORD];
ref_query_simi ret_query;

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
void closeBinFile(){
    close(gBinFd);
}
int query_db(simility ptr_fun, float * feature_query, float thresh, ref_query_simi * pRef_query_result){
    int ret = 0;
    record record_a;
    int numRecode=0,i,rval,cnt=0;
    float simi;
	do{
        readNumRecords(&gBinFd, &numRecode);
        lseek(gBinFd,BTYES_NUM_RECOEDS,SEEK_SET);//start+
        for(i=0;i<numRecode;i++){
            rval = read(gBinFd,&record_a,BTYES_A_RECOEDS);
            if(rval != BTYES_A_RECOEDS){
                printf("read file error\n");
                ret = -1;
                break;
            }
            simi = (*ptr_fun)(feature_query,record_a.feature,128);
            //printf("name:%s,simi:%f\n",record_a.name,simi);
            if(simi >= thresh){//find it
                if(MAX_NUM_RECORD>cnt){
                    strncpy(ret_query_[cnt].name, record_a.name, sizeof(ret_query_[cnt].name)-1);
                    ret_query_[cnt].simility = simi;
                    cnt++;
                }
            }
        }
        ret_query.pQuery_simi = ret_query_;
        ret_query.ret_query_num = cnt;
        pRef_query_result = &ret_query; 
    }while(0);
	
	return ret;
}
int Top_one(ref_query_simi *pRef_query_simi_){
    float max = -100;
    int i=0,index=0,len=pRef_query_simi_->ret_query_num;

    for(i =0;i<len;i++)
    {
        if(pRef_query_simi_->pQuery_simi[i].simility>=max)
        {
            max = pRef_query_simi_->pQuery_simi[i].simility;
            index=i;
        }
    }

    return index;
}
void swap_f(float *xp, float *yp) 
{ 
    float temp = *xp; 
    *xp = *yp; 
    *yp = temp; 
}
void swap_i(int *xp, int *yp) 
{ 
    int temp = *xp; 
    *xp = *yp; 
    *yp = temp; 
}
void func_top_k(float * fea, int fea_len, int * idx_top, int top_k){
    int n=fea_len;
    int i, j, max_idx; 
    float * arr = (float *)malloc(sizeof(float)*fea_len);
    memcpy(arr,fea,sizeof(float)*fea_len);
    int * idx = (int *)malloc(sizeof(int)*fea_len);
    for(i = 0; i < n; i++)idx[i]=i;
    // One by one move boundary of unsorted subarray 
    for (i = 0; i < n-1; i++) 
    { 
        // Find the minimum element in unsorted array 
        max_idx = i; 
        for (j = i+1; j < n; j++) 
          if (arr[j] > arr[max_idx]) 
            max_idx = j; 
  
        // Swap the found minimum element with the first element 
        swap_f(&arr[max_idx], &arr[i]);
        swap_i(&idx[max_idx], &idx[i]); 
    }
    memcpy(idx_top,idx,sizeof(int)*top_k);
    free(arr);
    free(idx);
}
void Top_k(ref_query_simi *pRef_query_simi_,int * idx_top, int top_k){
    
    int len=pRef_query_simi_->ret_query_num;
    float * fea= (float *)malloc(sizeof(float)*len);
    for(int i =0;i<len;i++)fea[i]=pRef_query_simi_->pQuery_simi[i].simility;
    
    func_top_k(fea, len, idx_top, top_k);

    free(fea);
}
