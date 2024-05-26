#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    const int FAT = 512;
    // Report if the command is less than or more than 2
    if (argc != 2)
    {
        printf("One command line only!\n");
        return 1;
    }
    // Open card.raw
    FILE *card;
    card = fopen(argv[1], "r");
    // Report if not able to open the file
    if (card == NULL)
    {
        printf("Cannot open file!\n");
        return 1;
    }
    // Assign a 512 bytes buffer
    BYTE* buffer = malloc(sizeof(BYTE) * FAT);
    if (buffer == NULL)
    {
        printf("Could not access memory!");
        return 1;
    }

    // Create and open 000.jpeg
    int file_number = 0;
    char file_name[9] = "000.jpg";
    FILE* fp = fopen(file_name, "w");
    int already_writing = 0;

    // Read contents into buffer per 512 BYTEs
    while (fread(buffer, sizeof(BYTE), 512, card) == 512)
    {
        // If find out the sig
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            // and not yet writing, close the original file, open a new one then start writing
            if (already_writing)
            {
                fclose(fp);
                file_number += 1;
                file_name[0] = (char) (file_number / 100) + 48;
                file_name[1] = (char) (file_number / 10 - (file_number / 100) * 10) + 48;
                file_name[2] = (char) (file_number - (file_number / 10) * 10) + 48;
                fp = fopen(file_name, "w");
                fwrite(buffer, sizeof(BYTE), 512, fp);
            }
            // just write and assign state as already writing
            else
            {
                already_writing = 1;
                fwrite(buffer, sizeof(BYTE), 512, fp);
            }
        }
        // If the state is writing, keep writing
        else if (already_writing)
        {
            fwrite(buffer, sizeof(BYTE), 512, fp);
        }
    }
    // Free up memory and close opened files
    fclose(fp);
    fclose(card);
    free(buffer);
    return 0;
}
