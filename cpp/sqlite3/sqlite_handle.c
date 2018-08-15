#include "sqlite_handle.h"
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "sqlite3.h"

#define FILE_NAME_MAX_LEN 32
static sqlite3* recorder_db;

//@ common api------------------------------------------------------
int init_db(void) {
    int rc = 0;
    rc = sqlite3_open(RECORDER_DB_DIR, &recorder_db);
    if (rc) {
        printf("Can't open database: %s ", sqlite3_errmsg(recorder_db));
        sqlite3_close(recorder_db);
        return (1);
    }

    table_cfg data;
    if (find_db_cfg("UINIT", &data) == 0)
        return 0;

    char* zErrMsg = 0;
    char* sql_1 =
        "CREATE TABLE IF NOT EXISTS cfg(id INTEGER PRIMARY KEY AUTOINCREMENT,type TEXT NOT NULL,v0 TEXT NOT NULL, v1 TEXT NOT NULL, \
v2 TEXT NOT NULL, v3 TEXT NOT NULL,v4 TEXT NOT NULL, v5 TEXT NOT NULL,v6 TEXT NOT NULL, v7 TEXT NOT NULL,v8 TEXT NOT NULL, v9 TEXT NOT NULL, \
v10 TEXT NOT NULL, v11 TEXT NOT NULL,v12 TEXT NOT NULL, v13 TEXT NOT NULL,v14 TEXT NOT NULL, v15 TEXT NOT NULL,v16 TEXT NOT NULL, \
v17 TEXT NOT NULL,v18 TEXT NOT NULL, v19 TEXT NOT NULL,v20 TEXT NOT NULL, v21 TEXT NOT NULL,v22 TEXT NOT NULL, v23 TEXT NOT NULL, \
v24 TEXT NOT NULL, v25 TEXT NOT NULL,v26 TEXT NOT NULL, v27 TEXT NOT NULL,v28 TEXT NOT NULL, v29 TEXT NOT NULL);";
    sqlite3_exec(recorder_db, sql_1, 0, 0, &zErrMsg);
    if (zErrMsg) {
        printf("%s\n", zErrMsg);
    }
    char* sql_2 =
        "CREATE TABLE IF NOT EXISTS alert(id INTEGER PRIMARY KEY AUTOINCREMENT,type TEXT NOT NULL, time INTEEGER NOT NULL,faceID INTEGER NOT NULL, \
Video TEXT NOT NULL,Audio TEXT NOT NULL,Pic TEXT NOT NULL);";
    sqlite3_exec(recorder_db, sql_2, 0, 0, &zErrMsg);
    if (zErrMsg) {
        printf("%s\n", zErrMsg);
    }
    char* sql_3 =
        "CREATE TABLE IF NOT EXISTS face(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,dir INTEGER NOT NULL, \
feature blob NOT NULL);";
    sqlite3_exec(recorder_db, sql_3, 0, 0, &zErrMsg);
    if (zErrMsg) {
        printf("%s\n", zErrMsg);
    }

    //批量初始化插入
    char* cmd[8] = {"UINIT", "USNYJ", "USWYJ", "UWPJK",
                    "UYLY",  "UISPC", "UGNKA", "UYTKZ"};
    init_db_cfg(cmd, 8);

    return rc;
}

void close_db() {
    sqlite3_close(recorder_db);
}

int drop_table(char* table_name) {
    char* zErrMsg = 0;
    char sql[255];
    sprintf(sql, "drop table if exists %s", table_name);
    sqlite3_exec(recorder_db, sql, 0, 0, &zErrMsg);
    if (zErrMsg != NULL)
        printf("%s\n", zErrMsg);
    return 0;
}

//@ table cfg api---------------------------
void table_cfg_print(table_cfg data) {
    int i = 0;
    printf("id:%d,type:%s ", data.id, data.type);
    for (i = 0; i < 30; i++) {
        printf("%s,", data.v_info[i]);
        if (i % 8 == 0)
            printf("\n");
    }
    printf("\n");
}

//写入数据库
int insert_db_cfg(table_cfg rows) {
    int ret;
    char insert_sql[400], *zErrMsg = 0;
    sprintf(
        insert_sql,
        "INSERT INTO cfg (type,v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22,v23,v24,v25,v26,v27,v28,v29) \
VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', \
'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')",
        rows.type, rows.v_info[0], rows.v_info[1], rows.v_info[2],
        rows.v_info[3], rows.v_info[4], rows.v_info[5], rows.v_info[6],
        rows.v_info[7], rows.v_info[8], rows.v_info[9], rows.v_info[10],
        rows.v_info[11], rows.v_info[12], rows.v_info[13], rows.v_info[14],
        rows.v_info[15], rows.v_info[16], rows.v_info[17], rows.v_info[18],
        rows.v_info[19], rows.v_info[20], rows.v_info[21], rows.v_info[22],
        rows.v_info[23], rows.v_info[24], rows.v_info[25], rows.v_info[26],
        rows.v_info[27], rows.v_info[28], rows.v_info[29]);

    ret = sqlite3_exec(recorder_db, insert_sql, NULL, 0, &zErrMsg);

    if (ret != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        return 1;
    }

    return 0;
}

//批量写入type
int init_db_cfg(char** cmd, int len) {
    int i;
    /* 手动开启事物 */
    sqlite3_stmt* stmtb = NULL;
    const char* beginSQL = "BEGIN TRANSACTION";
    if (sqlite3_prepare_v2(recorder_db, beginSQL, strlen(beginSQL), &stmtb,
                           NULL) != SQLITE_OK) {
        if (stmtb)
            sqlite3_finalize(stmtb);
        sqlite3_close(recorder_db);
        return 1;
    }
    if (sqlite3_step(stmtb) != SQLITE_DONE) {
        sqlite3_finalize(stmtb);
        sqlite3_close(recorder_db);
        return 1;
    }
    sqlite3_finalize(stmtb);
    /*****************************/

    char* err_msg = 0;
    // char* sql = "INSERT INTO cfg(type) VALUES(?)";
    char* sql =
        "INSERT INTO cfg (type,v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22,v23,v24,v25,v26,v27,v28,v29) \
VALUES (?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) ";
    sqlite3_stmt* stmt = NULL;
    if (sqlite3_prepare_v2(recorder_db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        if (stmt)
            sqlite3_finalize(stmt);
        sqlite3_close(recorder_db);
        return 1;
    }

    for (i = 0; i < len; i++) {
        sqlite3_bind_text(stmt, 1, cmd[i], -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            sqlite3_close(recorder_db);
            return 1;
        }
        sqlite3_reset(stmt);
    }
    sqlite3_finalize(stmt);

    /* 手动关闭事物 */
    sqlite3_stmt* stmtc = NULL;
    const char* commitSQL = "COMMIT TRANSACTION";
    if (sqlite3_prepare_v2(recorder_db, commitSQL, strlen(commitSQL), &stmtc,
                           NULL) != SQLITE_OK) {
        if (stmtc)
            sqlite3_finalize(stmt);
        sqlite3_close(recorder_db);
        return 1;
    }
    if (sqlite3_step(stmtc) != SQLITE_DONE) {
        sqlite3_finalize(stmtc);
        sqlite3_close(recorder_db);
        return 1;
    }
    sqlite3_finalize(stmtc);
    return 0;
}

static int gFound;
static int find_db_cfg_callback(void* data,
                                int argc,
                                char** argv,
                                char** azColName) {
    int i;
    table_cfg* rows = (table_cfg*)data;
    gFound = 0;
    rows->id = atoi(argv[0]);
    strcpy(rows->type, argv[1]);
    for (i = 2; i < argc; i++) {
        strcpy(rows->v_info[i - 2], argv[i]);
    }
    // table_cfg_print(*rows);
    return 0;
}

//查询cfg中type对应的配置
int find_db_cfg(char* cfgCode, table_cfg* rows) {
    int ret;
    gFound = 1;
    char sql[50], *zErrMsg = 0;

    sprintf(sql, "select * from cfg where type='%s' ", cfgCode);
    ret = sqlite3_exec(recorder_db, sql, find_db_cfg_callback, (void*)rows,
                       &zErrMsg);

    if (ret != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        return 1;
    }
    return gFound;
}

int get_db_cfg(table_cfg* rows) {
    char* pErrMsg = 0;
    int nrow = 0, ncolumn = 0;
    char** azResult;
    char sql[255];
    sprintf(sql, "select * from cfg where type='%s' ", rows->type);

    int ret = sqlite3_get_table(recorder_db, sql, &azResult, &nrow, &ncolumn,
                                &pErrMsg);
    if (pErrMsg) {
        printf("zErrMsg = %s\n", pErrMsg);
        return 1;
    }

    int index = ncolumn;
    int i, j;

    if (strcmp(rows->type, azResult[index + 1]) != 0) {
        //未查询到任何记录则返回-1
        sqlite3_free_table(azResult);
        return -1;
    }

    for (i = 0; i < nrow; i++) {
        rows->id = atoi(azResult[index++]);
        strcpy(rows->type, azResult[index++]);
        for (j = 0; j < ncolumn - 2; j++) {
            strcpy(rows->v_info[j], azResult[index++]);
        }
    }

#if 0
    printf("%s | %s\n", azResult[0], azResult[1]);
    printf("--------------------------------\n");
    int index = ncolumn;
    int i, j;
    for (i = 0; i < nrow; i++) {
        for (j = 0; j < ncolumn; j++) {
            printf("%-5s ", azResult[index++]);
        }
        printf("\n");
    }
    printf("--------------------------------\n");
#endif

    sqlite3_free_table(azResult);
    return 0;
}

//更新数据库
int update_db_cfg(char* cfgCode, table_cfg rows) {
    int ret, i;
    char sql[400], *zErrMsg = 0;
    sprintf(
        sql,
        "update cfg set v0='%s',v1='%s',v2='%s',v3='%s',v4='%s',v5='%s',v6='%s',v7='%s',v8='%s',v9='%s',v10='%s', \
v11='%s',v12='%s',v13='%s',v14='%s',v15='%s',v16='%s',v17='%s',v18='%s',v19='%s',v20='%s',v21='%s',v22='%s',v23='%s', \
v24='%s',v25='%s',v26='%s',v27='%s',v28='%s',v29='%s' where type='%s' ",
        rows.v_info[0], rows.v_info[1], rows.v_info[2], rows.v_info[3],
        rows.v_info[4], rows.v_info[5], rows.v_info[6], rows.v_info[7],
        rows.v_info[8], rows.v_info[9], rows.v_info[10], rows.v_info[11],
        rows.v_info[12], rows.v_info[13], rows.v_info[14], rows.v_info[15],
        rows.v_info[16], rows.v_info[17], rows.v_info[18], rows.v_info[19],
        rows.v_info[20], rows.v_info[21], rows.v_info[22], rows.v_info[23],
        rows.v_info[24], rows.v_info[25], rows.v_info[26], rows.v_info[27],
        rows.v_info[28], rows.v_info[29], cfgCode);

    ret = sqlite3_exec(recorder_db, sql, NULL, 0, &zErrMsg);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        return 1;
    }
    return 0;
}

//删除数据库,根据rows.type
int delete_db_cfg(char* cfgCode, table_cfg rows) {
    int ret;
    char sql[50], *zErrMsg = 0;
    memset(sql, 0, sizeof(char) * strlen(sql));
    sprintf(sql, "DELETE from cfg where type='%s'", cfgCode);

    ret = sqlite3_exec(recorder_db, sql, NULL, 0, &zErrMsg);

    if (ret != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        return 1;
    }
    return 0;
}

//@ table face api---------------------------
void table_face_print(table_face data) {
    int i = 0;
    printf("id:%d,name:%s,dir:%d\n", data.id, data.name, data.dir);
    for (i = 0; i < 5; i++)
        printf("first-5-fea:%f ", data.feature[i]);
    for (i = 5; i > 0; i--)
        printf("last-5-fea:%f ", data.feature[face_feature_lenght - i]);
}
//写入数据库
int insert_db_face(table_face _table_face) {
    sqlite3* db  = recorder_db;
    int ret;
    sqlite3_stmt* stmt = NULL;
    char sql[125];
    sprintf(sql, "INSERT INTO face(name, dir, feature) VALUES('%s', %d, ?)",
            _table_face.name, _table_face.dir);

    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n",
                ret, sqlite3_errmsg(db));

        return -1;
    }
    ret = sqlite3_bind_blob(stmt, 1, _table_face.feature,
                            face_feature_lenght * sizeof(float), NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "db bind blob fail, errcode[%d], errmsg[%s]\n", ret,
                sqlite3_errmsg(db));

        return -1;
    }

    ret = sqlite3_step(stmt);
    if (ret != SQLITE_DONE) {
        fprintf(stderr, "db insert fail, errcode[%d], errmsg[%s]\n", ret,
                sqlite3_errmsg(db));

        return -1;
    }

    sqlite3_finalize(stmt);
    return 0;
}
//查询数据库，获取特征值
int find_db_face(table_face* _table_face) {
    sqlite3* db = recorder_db;
    int ret;
    sqlite3_stmt* stmt = NULL;
    const unsigned char* name;
    float* feature;
    char sql[125];
    // int cnt = 0;
    sprintf(sql, "select * from face where name = '%s' and dir = %d;",
            _table_face->name, _table_face->dir);
    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n",
                ret, sqlite3_errmsg(db));
        return -1;
    }

    ret = SQLITE_ROW;
    int isFound = 0;
    while (1) {
        ret = sqlite3_step(stmt);
        if (ret == SQLITE_ROW) {
            name = sqlite3_column_text(stmt, 1);
            if (strcmp((const char*)name, _table_face->name) == 0) {
                feature =
                    (float*)(sqlite3_column_blob(stmt, 3));
                memcpy(_table_face->feature, feature,
                       face_feature_lenght * sizeof(float));
                _table_face->id = sqlite3_column_int(stmt, 0);
                _table_face->dir = sqlite3_column_int(stmt, 2);
                // printf("num:%d\n",++cnt);
                isFound = 1;
                break;
            }
        } else if (ret == SQLITE_DONE) {
            // printf("select done!\n");
            break;
        } else {
            fprintf(stderr, "db step fail, errcode[%d], errmsg[%s]\n", ret,
                    sqlite3_errmsg(db));
            return -1;
        }
    }

    sqlite3_finalize(stmt);
    return gFound;
}

float GetFaceFeatureSimility(float  *feature1,float  *feature2)
{
    if(feature1==NULL||feature2==NULL) 
    {    
         printf("In the func Classifier::GetFaceFeatureSimility(),the input param feature1 or feature2 is err!\n");
         return 0;
    }
    float sumarrayA=0,sumarrayB=0;
    float cosine=0;
    float *temp_feature1=(float *)feature1;
    float *temp_feature2=(float *)feature2;
    int temp_len=face_feature_lenght;
    
    int i;
    for(i=0;i<temp_len;i++)
    {
        sumarrayA+=temp_feature1[i]*temp_feature1[i];
        sumarrayB+=temp_feature2[i]*temp_feature2[i];
        cosine+=temp_feature1[i]*temp_feature2[i];
    }
    sumarrayA=sqrt(sumarrayA);
    sumarrayB=sqrt(sumarrayB);
    if((sumarrayA-0<0.0001)||(sumarrayB-0<0.0001))
    {
        //printf("In the func Recognition::GetFaceFeatureSimility(),the value of the input param feature1 or feature2 is 0!\n");
        return 0;
    }

    cosine =(cosine)/(sumarrayA*sumarrayB);
    return cosine;
}


//查询数据库，根据特征值计算相似度，返回符合阈值和给定数量的结果
int find_db_face_simility(simility ptr_fun,
                          float* feature,
                          table_face* p_table_face,
                          float* simility,
                          float thresh,
                          int len) {
    sqlite3* db  = recorder_db;
    int ret;
    float score;
    float* feature_;
    float simility_;
    int cnt = 0;
    sqlite3_stmt* stmt = NULL;
    char sql[125];
    const unsigned char* name;
    if (len < 1)
        return -1;
    sprintf(sql, "select * from face ");

    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n",
                ret, sqlite3_errmsg(db));
        // sqlite3_close(db);
        return -1;
    }

    ret = SQLITE_ROW;
    while (1) {
        ret = sqlite3_step(stmt);
        if (ret == SQLITE_ROW) {
            feature_ = (float*)(sqlite3_column_blob(stmt, 3));
            simility_ = (*ptr_fun)(feature, feature_);

            if (simility_ >= thresh) {
                (p_table_face + cnt)->id = sqlite3_column_int(stmt, 0);
                name = sqlite3_column_text(stmt, 1);
                strncpy((p_table_face + cnt)->name, (const char*)name,
                        strlen((const char*)name));
                (p_table_face + cnt)->dir = sqlite3_column_int(stmt, 2);
                memcpy((p_table_face + cnt)->feature, feature_,
                       face_feature_lenght * sizeof(float));
                simility[cnt] = simility_;
                if (++cnt == len)
                    break;
            }
        } else if (ret == SQLITE_DONE) {
            // printf("select done!\n");
            break;
        } else {
            fprintf(stderr, "db step fail, errcode[%d], errmsg[%s]\n", ret,
                    sqlite3_errmsg(db));
            return -1;
        }
    }

    sqlite3_finalize(stmt);
    return 0;
}

//更新数据库
int update_db_face(table_face _table_face) {
    int ret;
    sqlite3* db  = recorder_db;
    sqlite3_stmt* stmt = NULL;
    char sql[125];
    sprintf(sql, "UPDATE face set  feature=? WHERE dir = %d and name = '%s'",
            _table_face.dir, _table_face.name);

    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n",
                ret, sqlite3_errmsg(db));
        // sqlite3_close(db);
        return -1;
    }

    ret = sqlite3_bind_blob(stmt, 1, _table_face.feature,
                            face_feature_lenght * sizeof(float),
                            NULL);  // 1对应第一个问号
    if (ret != SQLITE_OK) {
        fprintf(stderr, "db bind blob fail, errcode[%d], errmsg[%s]\n", ret,
                sqlite3_errmsg(db));
        // sqlite3_close(db);
        return -1;
    }

    ret = sqlite3_step(stmt);
    if (ret != SQLITE_DONE) {
        fprintf(stderr, "db insert fail, errcode[%d], errmsg[%s]\n", ret,
                sqlite3_errmsg(db));
        // sqlite3_close(db);
        return -1;
    }

    sqlite3_finalize(stmt);
    return 0;
}

//删除数据库中的某个字段的数据
int delete_db_face(table_face _table_face) {
    sqlite3* db = recorder_db;
    int ret;
    sqlite3_stmt* stmt = NULL;
    char sql[125];
    sprintf(sql, "DELETE FROM face WHERE name = '%s' and dir = %d;",
            _table_face.name, _table_face.dir);

    ret = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (ret != SQLITE_OK) {
        fprintf(stderr, "sqlite3_prepare_v2 failed, errcode[%d], errmsg[%s]\n",
                ret, sqlite3_errmsg(db));
        // sqlite3_close(db);
        return -1;
    }

    ret = sqlite3_step(stmt);
    if (ret != SQLITE_DONE) {
        fprintf(stderr, "db insert fail, errcode[%d], errmsg[%s]\n", ret,
                sqlite3_errmsg(db));
        // sqlite3_close(db);
        return -1;
    }

    sqlite3_finalize(stmt);
    return 0;
}
