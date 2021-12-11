/**
 *  This code is intented to analyse the runtime complexity of the algorithm . 
 * Since it is proved theoritically that the complexity should be O(logn + k)
 * In this file we will check the complexity dependence of log(n)
 * 
 * Keep k as constant 
 * Stores all the runtimes in a file named logn_runtimes.txt
 */

#include "algo.c"


/******************** Creates an array from 1 to n ***********************/ 
void create_arr(int arr[] , int n){
    
    for (int i=0; i<n;i++) arr[i] = i; 

}



int main(){
    
    // choosing various values of n
    int n_val[100];
    float temp=1;
    float exp = 1.085; 
    for (int j=0; j< 100; j++){
        
        
        temp = temp* exp ;
        n_val[j] = (int)(100*temp);
    }


    int len = sizeof(n_val) / sizeof(n_val[0]);
    double total_time;
    int loops = 50;   // loops to take average of all runtimes for a particular setting to get stable results
    clock_t timer;

    FILE * fptr;
    fptr = fopen("./logn_runtimes.txt", "a");
    fptr=freopen(NULL,"w",fptr);

    for(int k=0; k < len; k++){

        int n = n_val[k]; 
        printf("%d\n", n);
        int arr[n];

        create_arr(arr,n);

        Node* root = (Node*)malloc(sizeof(Node));
        
        root = create_BBST(arr,0, n-1);
        total_time = 0;
        for(int loop=0; loop<loops; loop++){
         
        timer = clock();   // timer start
        traversal(root, -1,-1);
        
        timer = clock() - timer;  // timer stop 
        double time_taken = ((double)timer)/CLOCKS_PER_SEC;
        // printf("%.8f\t", time_taken);


        
        total_time+= time_taken; 
        }

        double avg_time_taken = total_time/loops;
        printf("\n");
        printf("%.10f\n", avg_time_taken);
        printf("\n");


        fprintf(fptr, "%d", n);
        fprintf(fptr, ",");
        fprintf(fptr, "%.10f", avg_time_taken);
        fprintf(fptr, "\n");
    }
    fclose(fptr);
}

