#include <stdio.h>
#include <stdlib.h>
#include<time.h>
#include<math.h>

struct bstnode
{
    int val;
    struct bstnode *left;
    struct bstnode *right;
};

typedef struct bstnode Node;

/*** Create a new node ***/
Node* new (int val)
{
    Node* node = (Node*)malloc(sizeof(Node));
    node-> val = val;
    node-> left = NULL;
    node -> right = NULL;
    return node;

}

/** Creating a Balanced BST from a sorted array**/
Node* create_BBST(int arr[], int start, int end){
    
    Node* temp = (Node*)malloc(sizeof(Node));
    if( start > end) return NULL;

    int mid = (start + end)/2;

    temp = new(arr[mid]);
    temp->left = create_BBST( arr, start, mid -1);
    temp->right = create_BBST( arr, mid+1, end);
    return temp;
    
}

void inorder(Node* temp){
    if (!temp)  return ;

    inorder(temp->left);
    printf("%d->", temp->val);
    inorder(temp->right);
}

void preorder(Node* temp){
    if (!temp)  return ;

    printf("%d->", temp->val);
    preorder(temp->left);
    preorder(temp->right);
}

void postorder(Node* temp){
    if (!temp)  return ;


    postorder(temp->left);
    postorder(temp->right);
    printf("%d->", temp->val);
}

void search(int val, Node* temp){
    if(!temp) {
        printf(" ");
        return;
    }


    else if (temp-> val == val){
        
        printf("%d",temp->val);
    }

    else if (temp-> val < val){
        printf("%d",temp->val);
        search(val, temp->right);
    }

    else{
        printf("%d",temp->val);
        search(val, temp->left);
    }
}


/******************** Creates an array from 1 to n ***********************/ 
void create_arr(int arr[] , int n){
    
    for (int i=0; i<n;i++) arr[i] = i; 

}

int main(){
    int n = 1000000;
    int loops = 100000;

    double total_time;
    double time_per_loop;
    double avg_time;

    clock_t timer;

    int arr[n];
    create_arr(arr,n);
    Node* root = (Node*)malloc(sizeof(Node));
    root = create_BBST(arr,0, n-1);

    total_time = 0;

    for(int loop=0; loop<loops; loop++){
        timer = clock();
        search(-1,root);
        timer = clock() - timer;
        time_per_loop = ((double)timer)/CLOCKS_PER_SEC;
        total_time += time_per_loop;
    }

    avg_time = total_time/loops;
    printf("\n%.10f\n", avg_time*1000000);

}

/*
int main(){
    // choosing various values of n
    int n_val[50];
    float temp=1;
    float exp = 1.1; 
    for (int j=0; j< 50; j++){
        
        
        temp = temp* exp ;
        n_val[j] = (int)(100*temp);
    }


    int len = sizeof(n_val) / sizeof(n_val[0]);
    double total_time;
    int loops = 10; 
    clock_t timer;

    FILE * fptr;
    fptr = fopen("./search_runtimes.txt", "a");
    fptr=freopen(NULL,"w",fptr);

    for(int k=0; k < len; k++){

        int n = n_val[k]; 
        printf("%d\n", n);
        int arr[n];

        create_arr(arr,n);
        // printf("%d\n", n);
        Node* root = (Node*)malloc(sizeof(Node));
        
        root = create_BBST(arr,0, n-1);
        total_time = 0;
        for(int loop=0; loop<loops; loop++){
         
        
        timer = clock();
        search(0,root);
        
        timer = clock() - timer;
        double time_taken = ((double)timer)/CLOCKS_PER_SEC;
        // printf("%.8f\t", time_taken);


        
        total_time+= time_taken; 
        }
        free(root);

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


}*/


/*
int main(){


    int arr[] = {4,10,12,15,18,22,24,25,31,35,44,50,66,70,90 };
    Node* root = (Node*)malloc(sizeof(Node));
    int n = sizeof(arr)/sizeof(arr[0]);
    int i;

    root = create_BBST(arr,0, n-1);
    search(90,root);

}*/