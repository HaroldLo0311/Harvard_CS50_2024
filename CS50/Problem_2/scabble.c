#include <stdio.h>
#include <ctype.h>
#include <string.h>

int score_calculator(char input_string[]);

int main(void)
{
    char input_1[100];
    char input_2[100];

    printf("Player 1: ");
    scanf("%s", input_1);

    printf("Player 2: ");
    scanf("%s[\n]", input_2);

    int score_1 = score_calculator(input_1);
    int score_2 = score_calculator(input_2);

    if (score_1 > score_2)
    {
        printf("Player 1 wins!");
    }
    else if (score_1 < score_2)
    {
        printf("Player 2 wins!");
    }
    else
    {
        printf("Tie!");
    }

}

int score_calculator(char input_string[])
{
    int length = strlen(input_string);
    char lower_string[100];
    int score = 0;
    // Get the words into lower case
    for (int i = 0; i < length; i++)
    {
        lower_string[i] = tolower(input_string[i]);
    }
    for (int i = 0; i < length; i++)
    {
        if (lower_string[i] == 'a' || lower_string[i] == 'e' || lower_string[i] == 'i' || lower_string[i] == 'l' || lower_string[i] == 'n' || lower_string[i] == 'o' || lower_string[i] == 'r' || lower_string[i] == 's' || lower_string[i] == 't' || lower_string[i] == 'u')
            score += 1;
        else if (lower_string[i] == 'd' || lower_string[i] == 'g')
            score += 2;
        else if (lower_string[i] == 'b' || lower_string[i] == 'c' || lower_string[i] == 'm' || lower_string[i] == 'p')
            score += 3;
        else if (lower_string[i] == 'f' || lower_string[i] == 'h' || lower_string[i] == 'v' || lower_string[i] == 'w' || lower_string[i] == 'y')
            score += 4;
        else if (lower_string[i] == 'k')
            score += 5;
        else if (lower_string[i] == 'j' || lower_string[i] == 'x')
            score += 8;
        else if (lower_string[i] == 'q' || lower_string[i] == 'z')
            score += 10;
    }
    return score;
}
