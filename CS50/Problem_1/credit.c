#include <stdio.h>

int main(void)
{
    char input_number[100];
    int is_alpha;
    int length;
    int checksum = 0;
    is_alpha = 1;

    // Make sure all elements in input_number are not alphabet
    while (is_alpha == 1)
    {
        printf("Number: ");
        scanf("%s", input_number);
        for (length = 0; input_number[length] != '\0'; ++length);

        for (int i = 0; i < length; i++)
        {
            // Input is not a number
            if (((input_number[i])) > 57 || (input_number[i]) < 48)
            {
                is_alpha = 1;
                break;
            }
            // Input is a number
            else
            {
                is_alpha = 0;
            }
        }
    }

    // Count the checksum:
    for (int i = length - 1; i >= 0; i--)
    {
        if ((length % 2 == 1 && i % 2 == 1) || (length % 2 == 0 && i % 2 == 0))
        {
            if (input_number[i] - 48 == 5)
                checksum += 1;
            else if (input_number[i] - 48 == 6)
                checksum += 3;
            else if (input_number[i] - 48 == 7)
                checksum += 5;
            else if (input_number[i] - 48 == 8)
                checksum += 7;
            else if (input_number[i] - 48 == 9)
                checksum += 9;
            else
                checksum += (input_number[i] - 48) * 2;
        }
        else
        {
            checksum += input_number[i] - 48;
        }
    }
    // Distinguish the credit card company
    if (checksum % 10 == 0)
    {
        // American Express:
        if (length == 15 && (input_number[0] - 48 == 3 && (input_number[1] - 48 == 4 || input_number[1] - 48 == 7)))
        {
            printf("AMEX\n");
        }
        // MasterCard :
        else if (length == 16 && (input_number[0] - 48 == 5 && (input_number[1] - 48 == 1 || input_number[1] - 48 == 2 || input_number[1] - 48 == 3 || input_number[1] - 48 == 4 || input_number[1] - 48 == 5)))
        {
            printf("MASTERCARD\n");
        }
        // Visa:
        else if ((length == 13 || length == 16) && input_number[0] - 48 == 4)
        {
            printf("VISA\n");
        }
        // Invalid
        else
        {
            printf("INVALID\n");
        }
    }
    // Invalid
    else
    {
        printf("INVALID\n");
    }
}