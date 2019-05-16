#ifndef _MYDATABASE_H
#define _MYDATABASE_H

#define	FILENAME_LENGTH	(256)
#define	NAME_LENGTH	FILENAME_LENGTH
#define	FEATURE_LENGTH	(128)

typedef struct record_t {
    char name[NAME_LENGTH];
    float feature[FEATURE_LENGTH];
}record;

#define BTYES_NUM_RECOEDS (sizeof(int))
#define BTYES_A_RECOEDS (sizeof(record))

extern int gBinFd;
extern char gDbFileName[FILENAME_LENGTH];

long get_file_size(const char *path);
int openBinFile(char *fname, int *pFd);
int addBinFile(record record_a);
int findBinFile(record * precord);
int deleteRecordByName(char *searchname);
int updateRecord(record  record_);

#endif
