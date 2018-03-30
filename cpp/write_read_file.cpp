#include <stdio.h>
#include <string.h>

int main()
{
    FILE * fp=fopen("./read_camera.txt","rb+");//以读/写方式打开一个二进制文件,文件形式x x
    
    char buf[50];
    int a,b;
    if(fp)
    {
        //先写入，然后读出
        sprintf(buf,"%d %d",1,0);
        fputs(buf,fp);
        //先读出，然后写入
        fgets(buf,50,fp);
        printf("out:%s\n",buf);
        sscanf(buf,"%d %d",&a,&b);
        printf("a:%d,b:%d\n",a,b);
        //先读出，然后写入
        fclose(fp);
    }
    else
    printf("file is not exists\n");
    
}
