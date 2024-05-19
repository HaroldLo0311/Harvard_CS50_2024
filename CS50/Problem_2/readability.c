#include <ctype.h>
#include <math.h>
#include <stdio.h>

int main(void)
{

    const int init_length = 1000;
    char init_story[init_length];

    char story[init_length];
    int total_letter = 0;
    int total_words = 0;
    int total_sentences = 0;
    float index = 0;

    for (int i = 0; i <= init_length; i++)
    {
        init_story[i] = ' ';
    }
    // Get the Text
    printf("Text: ");
    fgets(init_story, init_length, stdin);
    for (int i = 0; i <= init_length; i++)
    {
        story[i] = tolower(init_story[i]);
    }
    // Calculate total letters of the story
    for (int i = 0; i <= init_length; i++)
    {
        if (story[i] >= 'a' && story[i] <= 'z')
            total_letter += 1;
    }
    // Calculate number of word in the story
    for (int i = 0; i < init_length; i++)
    {
        if ((story[i] >= 'a' && story[i] <= 'z') && (story[i + 1] < 'a' || story[i + 1] > 'z') &&
            (story[i + 1] != '\'' && story[i + 1] != '-'))
            total_words += 1;
    }
    // Calculate number of sentence in the story
    for (int i = 0; i < init_length; i++)
    {
        if (story[i] == '.' || story[i] == '?' || story[i] == '!')
            total_sentences += 1;
    }
    // Apply Coleman-Liau index
    index = 0.0588 * 100 * total_letter / total_words -
            0.296 * 100 * total_sentences / total_words - 15.8;
    // Print the result
    printf("\ntotal letters: %i\n", total_letter);
    printf("total words: %i\n", total_words);
    printf("total sentences: %i\n", total_sentences);
    if (index < 1)
        printf("Before Grade 1\n");
    else if (index > 15)
        printf("Grade 16+\n");
    else
        printf("Grade %.0f\n", index);
}

