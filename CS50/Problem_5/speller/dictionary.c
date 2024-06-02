// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * 26 + 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_number = hash(word);
    // Initialize lowercase word array
    char low_word[LENGTH + 1] = {'\0'};
    for (int i = 0; i < strlen(word) + 1; i++)
    {
        low_word[i] = tolower(word[i]);
    }
    // Run through all nodes at the hash index
    for (node *ptr = table[hash_number]; ptr != NULL; ptr = ptr->next)
    {
        // While the word is found in dict
        if (strcmp(low_word, ptr->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Turn the first two input char into hash table
    if (isalpha(word[0]))
    {
        if (isalpha(word[1]))
            return (int) (toupper(word[1]) - 'A') + (int) (toupper(word[0]) - 'A') * 26 + 26;
        else
            return (int) (toupper(word[0]) - 'A');
    }
    else
        return N + 1;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *fptr = fopen(dictionary, "r");
    if (fptr == NULL)
    {
        return false;
    }
    char dict_word[LENGTH + 1] = {'\0'};
    char c;
    int i = 0;

    // Read words into buffer dict_word;
    c = getc(fptr);
    unsigned int hash_num = 0;
    while (c != EOF)
    {
        if (c == '\n' || c == ' ')
        {
            // Find the hash of the words
            hash_num = hash(dict_word);

            // String the linked list
            // 1. Create an new node
            node *new_node = malloc(sizeof(node));
            if (new_node == NULL)
            {
                return 1;
            }
            // 1.1 Initialize node
            new_node->next = NULL;
            for (int j = 0; j < LENGTH + 1; j++)
            {
                new_node->word[j] = '\0';
            }
            // 1.2 Write the dict word into the node
            for (int j = 0; j < LENGTH + 1; j++)
            {
                if (dict_word[j] != '\n' && dict_word[j] != '\0')
                    new_node->word[j] = dict_word[j];
            }
            // 2. Insert node to the front end of the corresponding hash
            if (table[hash_num] == NULL)
            {
                table[hash_num] = new_node;
            }
            else
            {
                new_node->next = table[hash_num];
                table[hash_num] = new_node;
            }
            // Reset the dict word buffer
            i = 0;
            c = getc(fptr);
            for (int j = 0; j < LENGTH + 1; j++)
            {
                dict_word[j] = '\0';
            }
        }
        dict_word[i] = c;
        i++;
        c = getc(fptr);
    }
    // Close file
    fclose(fptr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    unsigned int words_num = 0;
    // Run through all nodes and calculate the sum
    for (int i = 0; i < N; i++)
    {
        for (node *ptr = table[i]; ptr != NULL; ptr = ptr->next)
        {
            words_num++;
        }
    }
    return words_num;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Free all nodes
    for (int i = 0; i < N + 1; i++)
    {
        if (table[i] != NULL)
        {
            node *temp = table[i];
            while (temp != NULL)
            {
                node *next_node = temp->next;
                free(temp);
                temp = next_node;
            }
            free(temp);
        }
    }
    return true;
}
