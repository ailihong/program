#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <unistd.h>
#include <sys/ioctl.h>
//tutorial link :https://www.cnblogs.com/faraway/archive/2009/03/06/1404449.html
//----------------------TCP server code start---------------------------------------
int gServerSocketFd;
fd_set gFdReads;
#define MAX_CLINET_NUM 5
int gClientNum=0;
int gClientSocketFd[MAX_CLINET_NUM];
struct sockaddr_in gClientAddr[MAX_CLINET_NUM];
#define ServerPort 999
#define MAX_LISTEN 5
static pthread_t gServerThreadID;
static char gClientBuf[1500] = {0};

void * AcceptThread(void * pParam){
	int ret,i,j,numOfInvalid;
	int nMax_fd = 0;
	struct timeval timeout;
	socklen_t client_socket_size=sizeof(gClientAddr[0]);
	for(i=0;i<MAX_CLINET_NUM;i++){
		gClientSocketFd[i]=-1;
	}
	printf("start listening\n");
	ret = listen(gServerSocketFd, MAX_LISTEN);
	if(-1 == ret)
	{
		printf("listen socket error: %s errno : %d", strerror(errno), errno);
		return -1;
	}
	printf("goto loop\n");
	while(1){
		FD_ZERO(&gFdReads);
		
		FD_SET(gServerSocketFd, &gFdReads);//add server socket to focus

		nMax_fd = nMax_fd > gServerSocketFd ? nMax_fd : gServerSocketFd;
		for(i=0;i<gClientNum;i++){
			FD_SET(gClientSocketFd[i], &gFdReads);//add client socket to focus queue
			if(nMax_fd < gClientSocketFd[i])nMax_fd = gClientSocketFd[i];
		}
		//using select to check server
		timeout.tv_sec=30;
		timeout.tv_usec=0;

		ret = select(nMax_fd + 1, &gFdReads, 0, 0, &timeout);
		if (ret < 0) {
            perror("select");
            break;
        } else if (ret == 0) {
            printf("timeout\n");
            continue;
        }
		printf("select success\n");
		// check whether new data comes
		for(i=numOfInvalid=0;i<gClientNum;i++){
			if (FD_ISSET(gClientSocketFd[i], &gFdReads)){
				ret = recv(gClientSocketFd[i], gClientBuf, sizeof(gClientBuf), 0);
                if (ret <= 0) {        // client close
                    printf("client[%d] close\n", i);
                    close(gClientSocketFd[i]);
                    FD_CLR(gClientSocketFd[i], &gFdReads);
                    gClientSocketFd[i]=-1;
					numOfInvalid++;
                } else {        // receive data
                    if (ret < sizeof(gClientBuf))
                        memset(&gClientBuf[ret], '\0', 1);
                    	printf("client[%d] send:%s\n", i, gClientBuf);
                }
			}
		}
	#if 0
		if(numOfInvalid)
		printf("fd[%d %d %d %d %d]\n",gClientSocketFd[0],gClientSocketFd[1],gClientSocketFd[2]
		,gClientSocketFd[3],gClientSocketFd[4]);
	#endif
		//delete some closed client socket
		for(j=0;j<numOfInvalid;j++){
		for(i=0;i<gClientNum-1;i++){
			if(gClientSocketFd[i] == -1 && gClientSocketFd[i+1] != -1){
				gClientSocketFd[i] = gClientSocketFd[i+1];
				gClientSocketFd[i+1] = -1;
			}
		}
		}
	#if 0
		if(numOfInvalid)
		printf("after fd[%d %d %d %d %d]\n",gClientSocketFd[0],gClientSocketFd[1],gClientSocketFd[2]
		,gClientSocketFd[3],gClientSocketFd[4]);
	#endif
		if(numOfInvalid){
			gClientNum -= numOfInvalid;
			numOfInvalid = 0;
		}
		
		// check whether a new connection comes
        if (FD_ISSET(gServerSocketFd, &gFdReads)){
			if(gClientNum < MAX_CLINET_NUM){
				gClientSocketFd[gClientNum] = accept(gServerSocketFd, &gClientAddr[gClientNum], &client_socket_size);
				if(gClientSocketFd[gClientNum] <= 0){
					perror("accept");
					continue;
            	}
				gClientNum++;
				printf("accept success,client num:%d\n",gClientNum);
			}  
		}
	}
}
//----------------------TCP server code end---------------------------------------

int main()
{
	int ret = -1;
	int i,on=1;
  
	FD_ZERO(&gFdReads);
	//create tcp server
	gServerSocketFd = socket(AF_INET, SOCK_STREAM, 0);
	if(gServerSocketFd < 0)
	{
		printf("create socket error: %s errno : %d", strerror(errno), errno);
		return -1;
	}
	ret = ioctl(gServerSocketFd, FIONBIO, (char *)&on);//no blocking
	if (ret < 0)
	{
		perror("ioctl() failed\n");
		close(gServerSocketFd);
		return -1;
	}
   
	//bind addr and port
	struct sockaddr_in sockaddr;
	
	sockaddr.sin_family = AF_INET;
	sockaddr.sin_port = htons(ServerPort);
	sockaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	ret = bind(gServerSocketFd, &sockaddr, sizeof(sockaddr));
	if(-1 == ret)
	{
		printf("bind error: %s errno : %d", strerror(errno), errno);
		return -1;
	}

	ret = pthread_create(&gServerThreadID, NULL, &AcceptThread, (void *)NULL);
	if(ret)
	{
		printf("[%s:%d] pthread_create server net error [%d]\n", __FUNCTION__, __LINE__, ret);
		return -1;
	}
	pthread_join(gServerThreadID,NULL);
}
