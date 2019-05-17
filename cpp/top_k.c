#include <stdio.h>
#include <malloc.h>
#include <string.h>

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
void Top_k(float * fea, int fea_len, int * idx_top, int top_k){
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
int main()
{
    float fea[]={0.23,0.12,0.04,0.56,0.78, 0.00,0.00,0.56,0.33,0.44, 0.56,0.00,0.22};
    int fea_len = sizeof(fea)/sizeof(fea[0]);
    
    int idx[5]={0,0};
    Top_k(fea,fea_len,idx,5);
    for(int i =0 ;i<5;i++)
    printf("%d,%f\n",idx[i],fea[idx[i]]);
    return 0;
}
