#include <stdio.h>

int main(){
    int a, b;
    float c, d;

    a = 13;
    b = 5;

    c = a / b;
    d = (float) a / (float) b;

    printf("[integers] a = %d, b = %d\n", a, b);
    printf("[floats] c = %f, d = %f\n", c, d);
}