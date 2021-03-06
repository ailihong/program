#include "sqlite_db.h"

//写入数据库
int insert_db(sqlite3* db, const char * name, float* features)
{
    int ret;    
    const char * char_name = name;
    sqlite3_stmt * stmt = NULL;
    char sql[125] = "INSERT INTO face(name, feature) VALUES(?, ?)";
    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }

    ret = sqlite3_bind_text(stmt, 1, char_name, strlen(char_name),NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "db bind text fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
    ret = sqlite3_bind_blob(stmt, 2, features,  face_feature_lenght*sizeof(float), NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "db bind blob fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
    
    ret = sqlite3_step(stmt);
    if (ret != SQLITE_DONE) {
        fprintf(stderr, "db insert fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
 
    sqlite3_finalize(stmt);
    return 0;
}
//删除数据库中的某个字段的数据
int delete_db(sqlite3* db, const char * name)
{
    int ret;
    const char * char_name=name;
    sqlite3_stmt * stmt = NULL;
    char sql[125] = "DELETE FROM face WHERE name = ?";
    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }

    ret = sqlite3_bind_text(stmt, 1, char_name, strlen(char_name),NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "db bind text fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
    
    ret = sqlite3_step(stmt);
    if (ret != SQLITE_DONE) {
        fprintf(stderr, "db insert fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
 
    sqlite3_finalize(stmt);
    return 0;
}
//查询数据库,根据相似度阈值查询
int  query_db(sqlite3* db, simility ptr_fun, float * feature_query,char * ret_name[],float * ret_simility,float thresh,int * ret_len)
{
    int ret;
    float score;
    const unsigned char *name;
    float *feature;
    float simility;
    int cnt = 0;
    sqlite3_stmt * stmt = NULL;
    char sql[125] = "select * from face";
    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }

    ret = SQLITE_ROW;
    while(1){
        ret = sqlite3_step(stmt);
        if (ret == SQLITE_ROW) {
            name = sqlite3_column_text(stmt,1);
            //printf("name: %s,name_len:%d\nfeature:\n", name,strlen((const char *)name));
            feature = (float *)const_cast<void*>(sqlite3_column_blob(stmt, 3));
            /*for(int i=0;i<face_feature_lenght;i++)
            printf("%f \n",feature[i]);*/
            simility = (*ptr_fun)(feature_query,feature);
            //printf("score: %f\n", simility);
            
            if(simility >= thresh)
            {
                strncpy((char *)ret_name[cnt], (const char *)name, strlen((const char *)name));
                
                ret_simility[cnt] = simility;
                *ret_len = ++cnt;
            }
        }
        else if (ret == SQLITE_DONE) {
            printf("select done!\n");
            break;
        } else {
            fprintf(stderr, "db step fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
            break;
        }    
    }  
 
    sqlite3_finalize(stmt);
    return 0;
}
//查询数据库，获取特征值
int  query_get_feature(sqlite3* db, char * name_query,float * ret_feature)
{
    int ret;
    const unsigned char *name;
    float *feature;
    int cnt = 0;
    sqlite3_stmt * stmt = NULL;
    char sql[125] = "select * from face";
    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }

    ret = SQLITE_ROW;
    while(1){
        ret = sqlite3_step(stmt);
        if (ret == SQLITE_ROW) {
            name = sqlite3_column_text(stmt,1);
            if(strcmp((const char *)name,name_query)==0)
            {
                feature = (float *)const_cast<void*>(sqlite3_column_blob(stmt, 3));
                memcpy(ret_feature,feature,face_feature_lenght*sizeof(float));
            }
        }
        else if (ret == SQLITE_DONE) {
            printf("select done!\n");
            break;
        } else {
            fprintf(stderr, "db step fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
            break;
        }    
    }  
 
    sqlite3_finalize(stmt);
    return 0;
}
//更新数据库中的某个字段的数据
int update_db(sqlite3* db, const char * name, float* features)
{
    int ret;    
    const char * char_name=name;
    
    sqlite3_stmt * stmt = NULL;
    char sql[125] = "UPDATE face set feature = ? WHERE name = ?";
    
    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }

    ret = sqlite3_bind_blob(stmt, 1, features,  face_feature_lenght*sizeof(float), NULL);//1对应第一个问号
    if (ret != SQLITE_OK) {
        fprintf(stderr, "db bind blob fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }

    ret = sqlite3_bind_text(stmt, 2, char_name, strlen(char_name),NULL);//2对应第2个问号
    if (ret != SQLITE_OK) {
        fprintf(stderr, "db bind text fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
    
    ret = sqlite3_step(stmt);
    if (ret != SQLITE_DONE) {
        fprintf(stderr, "db insert fail, errcode[%d], errmsg[%s]\n", ret, sqlite3_errmsg(db));
        sqlite3_close(db);
        return -1;
    }
 
    sqlite3_finalize(stmt);
    return 0;
}
