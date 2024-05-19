
#include <string.h>
#include <ctype.h>
#include <stdio.h>


int main(int argc, char* argv[])
{
    // If the input is not adequate
    // If the input command number is wrong
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    const int char_num = 26;
    int length = strlen(argv[1]);
    char encoder[char_num];
    char input[1000];
    // If the input code number is wrong
    if (length < char_num)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    for (int i = 0; i < length; i++)
    {
        encoder[i] = toupper(argv[1][i]);
    }
    // If the input code have invalid char
    for (int i = 0; i < length; i++)
    {
        if (encoder[i] < 'A' || encoder[i] > 'Z')
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }
    for (int i = 0; i < length - 1; i++)
    {
        for (int j = 1; j < length; j++)
        {
            if ((i!= j) && (encoder[i] == encoder[j]))
            {
                printf("Usage: ./substitution key\n");
                return 1;
            }
        }
    }
    printf("plaintext: ");
    fgets(input, 100, stdin);
    int input_length = strlen(input) - 1;
    char output[input_length];
    // encode the input string
    for (int i = 0; i < input_length; i++)
    {
        char c = toupper(input[i]);
        if (c >= 'A' && c <= 'Z')
        {
            int ascii_number = c;
            if (islower(input[i]))
            {
                output[i] = tolower(encoder[ascii_number - 65]);
            }
            else
            {
                output[i] = encoder[ascii_number - 65];
            }
        }
        else
        {
            output[i] = input[i];
        }
    }
    printf("ciphertext: ");
    // Only print as long as the input length
    for (int i = 0; i < input_length; i++)
    {
        printf("%c", output[i]);
    }
    printf("\n");
    return 0;
}


