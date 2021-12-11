#include <stdio.h>
#include <stdlib.h>
#include<time.h>
#include<math.h>

/*** defining the structure of a node in a tree ***/
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


/**** Range search algorithm***/
void traversal(Node* temp, int a, int b){


    if(!temp) {return ;}

    else{
        if(temp->val <= a){
            
            if(temp->val == a){
                printf("%d--", a); // reporting by printing
            }
            traversal(temp->right, a, b);// ignoring the left subtree
        }


        else if(temp-> val >= b){
            //printf("%d--",temp->val); //uncomment during runtime_wrt_n analysis
            traversal(temp->left, a, b); // ignoring the right subtree
            if(temp->val == b){
                printf("%d--", b); // reporting by printing
            } 
        }

        else{
            traversal(temp->left, a, b);
            printf("%d--", temp->val); // reporting by printing
            traversal(temp->right, a, b);
        }
    }

    
}


int main(){


    int arr[] = {4,10,12,15,18,22,24,25,31,35,44,50,66,70,90 };
    Node* root = (Node*)malloc(sizeof(Node));
    int n = sizeof(arr)/sizeof(arr[0]);
    int i;

    printf("Given sorted array is :  \n");
    for (i=0; i<n;i++){
        printf("%d", arr[i]);
        printf(","); 
    }

    root = create_BBST(arr,0, n-1);
    int a = 19, b= 36; 

    printf("\n \n The elements in the range [%d, %d] of BBST is : \n", a,b);
    printf("\n");
    traversal(root,a,b);
    return 0;

}



