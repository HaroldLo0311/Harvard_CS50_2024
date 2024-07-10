import csv
import itertools
import sys
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
    # Ensure probabilities sum to 1
    normalize(probabilities)
    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def parent_prob_gene_gen(parent, one_gene, two_genes):
    # The function returns the prob of parent generating the gene
    if parent in one_gene:
        return 0.5
    elif parent in two_genes:
        return 1-PROBS['mutation']
    else:
        return PROBS['mutation']

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # count the prob of : 1. people have one_gene w/wo trait
    #                     2. people have two_genes w/wo trait
    # 1.People with parents:
    p_with_parent = set()
    for p in people:
        if people[p]['father'] != None:
            p_with_parent.add(p)
    # 2.Set up probability condition:
    condition = list()
    #3. List out the prob to give out gene:

    for p in people:
        # 1.Prob condition for people w/o parent:
        if p not in p_with_parent:
            if p in one_gene:
                condition += [PROBS['gene'][1]]
            elif p in two_genes:
                condition += [PROBS['gene'][2]]
            else:
                condition += [PROBS['gene'][0]]
        # 2.Prob condition for people w parent:
        else:
            prob_of_parent = 1
            if p in one_gene:
                # if person have one gene, passed by either father of mother
                prob_of_parent *= [parent_prob_gene_gen(people[p]['father'], one_gene, two_genes)* (1-parent_prob_gene_gen(people[p]['mother'], one_gene, two_genes)) + (1-parent_prob_gene_gen(people[p]['father'], one_gene, two_genes))* parent_prob_gene_gen(people[p]['mother'], one_gene, two_genes)]
            elif p in two_genes:
                # if person have two genes, pass by both father and mother
                prob_of_parent *= [parent_prob_gene_gen(people[p]['father'], one_gene, two_genes)* parent_prob_gene_gen(people[p]['mother'], one_gene, two_genes)]
            else:
                # if person have no gene, neither father nor mother passing
                prob_of_parent *= [(1-parent_prob_gene_gen(people[p]['father'], one_gene, two_genes))* (1-parent_prob_gene_gen(people[p]['mother'], one_gene, two_genes))]
            condition += prob_of_parent
        # 3.Add in the prob of w/wo trait
        if p in one_gene:
            condition += [PROBS['trait'][1][p in have_trait]]
        elif p in two_genes:
            condition += [PROBS['trait'][2][p in have_trait]]
        else:
            condition += [PROBS['trait'][0][p in have_trait]]
    joint_prob = 1
    for x in condition:
        joint_prob *= x
    return joint_prob



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]['gene'][1] += p
            probabilities[person]['trait'][person in have_trait] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
            probabilities[person]['trait'][person in have_trait] += p
        else:
            probabilities[person]['gene'][0] += p
            probabilities[person]['trait'][person in have_trait] += p
    return probabilities

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Update the sum of gene prob and train prob
        gene_prob_sum = 0
        trait_prob_sum = 0
        for gene_num in probabilities[person]['gene']:
            gene_prob_sum += probabilities[person]['gene'][gene_num]
        for trait_num in probabilities[person]['trait']:
            trait_prob_sum += probabilities[person]['trait'][trait_num]
        # Normalize
        for gene_num in probabilities[person]['gene']:
            probabilities[person]['gene'][gene_num] /= gene_prob_sum
        for trait_num in probabilities[person]['trait']:
            probabilities[person]['trait'][trait_num] /= trait_prob_sum
    return probabilities
if __name__ == "__main__":
    main()
