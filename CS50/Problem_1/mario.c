#include <stdio.h>

int main(void)
{
    int height;
    printf("Height: ");
    scanf("%d", &height);
    while (height <1 || height >8)
    {
        printf("Height: ");
        scanf("%d", &height);
    }

    for(int i = 0; i<height; i++)
    {
        for (int j = height-i-2; j>=0; j--)
        {
            printf(" ");
        }
        for (int k = 0; k<i+1; k++)
        {
            printf("#");
        }
        printf("  ");
        for (int k = 0; k<i+1; k++)
        {
            printf("#");
        }

        printf("\n");
    }

    return 0;
}