#include <stdio.h>
#include <unistd.h>

int main(){
    printf("real UID: %d\n", getuid());
    printf("effective UID: %d\n", geteuid());
}