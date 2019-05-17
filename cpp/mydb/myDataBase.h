#ifndef _MYDATABASE_H
#define _MYDATABASE_H

#define	FILENAME_LENGTH	(256)
#define	NAME_LENGTH	FILENAME_LENGTH
#define	FEATURE_LENGTH	(128)

typedef struct record_t {
    char name[NAME_LENGTH];
    float feature[FEATURE_LENGTH];
}record;

typedef struct query_simi_t{
char name[NAME_LENGTH];
float simility;
}query_simi;

typedef struct ref_query_simi_t{
    query_simi * pQuery_simi;
    int ret_query_num;
}ref_query_simi;

//返回值(*指针名)(参数列表)
typedef float (*simility)(float *,float *, int len);
extern ref_query_simi ret_query;

#define BTYES_NUM_RECOEDS (sizeof(int))
#define BTYES_A_RECOEDS (sizeof(record))

long get_file_size(const char *path);
// int openBinFile(char *fname, int *pFd);
int openBinFile_global(char *fname);
int addBinFile(record record_a);
int findBinFile(record * precord);
int deleteRecordByName(char *searchname);
int updateRecord(record  record_);
void closeBinFile();

int query_db(simility ptr_fun, float * feature_query, float thresh, ref_query_simi * pRef_query_result);
int Top_one(ref_query_simi *pRef_query_simi_);
void Top_k(ref_query_simi *pRef_query_simi_,int * idx_top, int top_k);
#endif
