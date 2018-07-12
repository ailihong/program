C string containing a file access mode. It can be:
"r"	read: Open file for input operations. The file must exist.
"w"	write: Create an empty file for output operations. If a file with the same name already exists, 
        its contents are discarded and the file is treated as a new empty file.
"a"	append: Open file for output at the end of a file. Output operations always write data at 
        the end of the file, expanding it. Repositioning operations (fseek, fsetpos, rewind) are ignored. 
	The file is created if it does not exist.
"r+"	read/update: Open a file for update (both for input and output). The file must exist.
"w+"	write/update: Create an empty file and open it for update (both for input and output). 
	If a file with the same name already exists its contents are discarded and the file 
	is treated as a new empty file.
"a+"	append/update: Open a file for update (both for input and output) with all output 
        operations writing data at the end of the file. Repositioning operations (fseek, fsetpos, rewind) 
	affects the next input operations, but output operations move the position back to the end of file.
	The file is created if it does not exist.
With the mode specifiers above the file is open as a text file. In order to open a file as a binary file, 
a "b" character has to be included in the mode string. This additional "b" character can either be appended 
at the end of the string (thus making the following compound modes: "rb", "wb", "ab", "r+b", "w+b", "a+b") 
or be inserted between the letter and the "+" sign for the mixed modes ("rb+", "wb+", "ab+").

//读写文件
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

//写duoble到二进制文件，然后读取
#include <stdio.h>
#include <string.h>

int main()
{
    double fnum[4] = {9.5, -3.4, 1.0, 2.1};
    FILE * fp=fopen("./test","wb+");
    if(fp)
    {
	fwrite( (char *)fnum, sizeof( double ), 4, fp );
        
    }
    else printf("file is not exists\n");
    fclose(fp);
    
    fp=fopen("./test","rb+");
    double fnum2[4] = {0};

    for(int i =0 ;i<4;i++)
    	printf("%lf ",fnum2[i]);
    if(fp)
    {
        
	fread( (char *)fnum2, sizeof( double ), 4, fp );
        
    }
    else printf("file is not exists\n");
    fclose(fp);
    for(int i =0 ;i<4;i++)
    	printf("%lf ",fnum2[i]);
    
}

fgets(buff, sizeof(buff) - 1, fp); // 包含了\n,读取一行
