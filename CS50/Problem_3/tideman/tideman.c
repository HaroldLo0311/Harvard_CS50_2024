#include <cs50.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        record_preferences(ranks);
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();

    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // if the name is valid, update name and return true, else return false
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // counting from rank 0, which is represented as i
    for (int i = 0; i < candidate_count - 1; i++)
    {
        // the later candidates are all less prefered comparing to current candidate
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]] += 1;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int pairs_index = 0;
    // if the candidate i is more preference than candidate j, then winner should be i and loser
    // should be j
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if ((i != j) && (preferences[i][j] > preferences[j][i]))
            {
                pairs[pairs_index].winner = i;
                pairs[pairs_index].loser = j;
                pairs_index += 1;
            }
        }
    }
    pair_count = pairs_index;
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // Bubble sort
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - 1; j++)
        {
            if (preferences[pairs[j].winner][pairs[j].loser] <
                preferences[pairs[j + 1].winner][pairs[j + 1].loser])
            {
                int winner_temp = pairs[j].winner;
                int loser_temp = pairs[j].loser;
                pairs[j].winner = pairs[j + 1].winner;
                pairs[j].loser = pairs[j + 1].loser;
                pairs[j + 1].winner = winner_temp;
                pairs[j + 1].loser = loser_temp;
            }
        }
    }

    return;
}

bool is_cycle(int test_winner, int test_loser)
{
    // Base case, if there the loser connect back to winner, there's circle
    if (locked[test_loser][test_winner] == true)
    {
        return true;
    }
    // Or if the test loser connect to other point, and the other point connect back to test winner
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[test_loser][i] == true && is_cycle(test_winner, i))
        {
            return true;
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Test each sorted pairs into the is_cycle function with reverse order
    for (int i = 0; i < pair_count; i++)
    {
        // Lock pair and check if it cause circle
        locked[pairs[i].winner][pairs[i].loser] = true;
        bool result = is_cycle(pairs[i].winner, pairs[i].loser);
        // If forming cycle, mark as false
        if (result == true)
        {
            locked[pairs[i].winner][pairs[i].loser] = false;
        }
    }
    return;
}

void print_winner(void)
{
    // If all bool in an y axis of lock is false, means no other candidates are preferred against
    // him
    for (int i = 0; i < candidate_count; i++)
    {
        int false_count = 0;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == false)
            {
                false_count += 1;
            }
        }
        if (false_count == candidate_count)
        {
            printf("%s\n", candidates[i]);
        }
    }
    return;
}
