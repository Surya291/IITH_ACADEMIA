/**
 *  This code is intented to analyse the runtime complexity of the algorithm . 
 * Since it is proved theoritically that the complexity should be O(logn + k)
 * In this file we will check the complexity dependence of k
 * 
 * Keep n = 10000 as constant
 * Stores all the runtimes in a file named logn_runtimes.txt
 */

#include "algo.c"


/******************** Creates an array from 1 to n ***********************/ 
void create_arr(int arr[] , int n){
    
    for (int i=0; i<n;i++) arr[i] = i; 

}



int main(){
    
    // seting n as constant = 10000
    int n_val[] = {10000};
    int k_val[100];
    for (int j=0; j<100; j++){
        k_val[j] = (1+j)*100;
    }



    int len = sizeof(k_val) / sizeof(k_val[0]);
    double total_time;
    int loops = 100; 
    int i; 
    clock_t timer;
    FILE * fptr;
    fptr = fopen("./k_runtimes.txt", "a");
    fptr=freopen(NULL,"w",fptr);

    for(i=0; i < len; i++){

        int n = n_val[0];
        int k = k_val[i]; 
        printf("%d\n", k);

        int arr[n];
        create_arr(arr,n);

        Node* root = (Node*)malloc(sizeof(Node));
        
        root = create_BBST(arr,0, n-1); // creating the BBST
        total_time = 0;
        for(int loop=0; loop<loops; loop++){
         
        timer = clock();
        traversal(root, 0,k); // traversing 
        
        timer = clock() - timer;
        double time_taken = ((double)timer)/CLOCKS_PER_SEC;
        // printf("%.8f\t", time_taken);
        total_time+= time_taken; 
        }


        double avg_time_taken = total_time/loops;
        printf("\n");
        printf("%.10f\n", avg_time_taken);
        printf("\n");


        fprintf(fptr, "%d", k);
        fprintf(fptr, ",");
        fprintf(fptr, "%.10f", avg_time_taken);
        fprintf(fptr, "\n");
        

    }
    fclose(fptr);
}

