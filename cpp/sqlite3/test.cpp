#include "sqlite_db.h"

#include "math.h"

sqlite3 *pdb;
float GetFaceFeatureSimility(float  *feature1,float  *feature2);

int main()
{
    
    int fd;
    fd = sqlite3_open("../face.db", &pdb);
    if (fd)
    {
        printf("can not open database!\n");
        sqlite3_close(pdb);
        return -1;
    }
    //insert name=123
    char* name = "123";
    float fea[face_feature_lenght];
    for(int i = 0;i<face_feature_lenght;i++)fea[i] = i;

    insert_db(pdb, name, fea);
    memset(fea,0,face_feature_lenght*sizeof(float));

    query_get_feature(pdb, name,fea);
    printf("after:\n");
    for(int i = 0;i<face_feature_lenght;i++)printf("%f\n",fea[i]);
    //insert name=456
    char* name2 = "456";
    float fea2[face_feature_lenght];
    for(int i = 0;i<face_feature_lenght;i++)fea2[i] = i%8;

    insert_db(pdb, name2, fea2);
    //delete
    delete_db(pdb, name2);
    
    memset(fea2,0,face_feature_lenght*sizeof(float));
    query_get_feature(pdb, name2,fea2);
    printf("after:\n");
    for(int i = 0;i<face_feature_lenght;i++)printf("%f\n",fea2[i]);

    //update
    update_db(pdb, name, fea2);
    memset(fea2,1,face_feature_lenght*sizeof(float));
    query_get_feature(pdb, name,fea2);

    printf("after:\n");
    for(int i = 0;i<face_feature_lenght;i++)printf("%f\n",fea2[i]);

    update_db(pdb, name, fea);
    //query
    float fea3[face_feature_lenght];
    for(int i = 0;i<face_feature_lenght;i++)fea3[i] = i-0.5;

    char names[MAX_NAME_NUM_IN_DATABASE][MAX_NAME_LENGHT];
    char *names_ptr[MAX_NAME_NUM_IN_DATABASE];
    for(int i = 0;i<MAX_NAME_NUM_IN_DATABASE;i++)
    {
        names_ptr[i] = names[i];
    }

    float simility[MAX_NAME_NUM_IN_DATABASE];
    int num=0;
    query_db(pdb, GetFaceFeatureSimility, fea3,names_ptr,simility,0.5,&num);
    printf("num:%d\n",num);
    if(num>0)
    {
        for(int i = 0;i<num;i++)
        printf("%s,%f\n",names[i],simility[i]);
    }
    
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
    
    for(int i=0;i<temp_len;i++)
    {
        sumarrayA+=temp_feature1[i]*temp_feature1[i];
        sumarrayB+=temp_feature2[i]*temp_feature2[i];
        cosine+=temp_feature1[i]*temp_feature2[i];
    }
    sumarrayA=sqrt(sumarrayA);
    sumarrayB=sqrt(sumarrayB);
    if((sumarrayA-0<0.0001)||(sumarrayB-0<0.0001))
    {
        printf("In the func Recognition::GetFaceFeatureSimility(),the value of the input param feature1 or feature2 is 0!\n");
        return 0;
    }

    cosine =fabs(cosine)/(sumarrayA*sumarrayB);
    return cosine;
}
