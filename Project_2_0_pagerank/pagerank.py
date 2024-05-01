import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {page_name: 0 for page_name in corpus}

    # If no page linked, the prob is equal
    if len(corpus[page]) == 0:
        for page_name in model:
            model[page_name] = 1/len(corpus)
        return model
    # Else add up the defined prob
    else:
        for page_name in model:
            model[page_name] = (1-damping_factor)/len(corpus)
        for linked_page in corpus[page]:
            model[linked_page] += damping_factor / len(corpus[page])
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_sampled = {page_sample:0 for page_sample in corpus}
    input_page = random.choice(list(corpus))
    sample_count = 0
    next_page = 0
    while sample_count < n:
        prob = random.random()
        # Page number count +1
        pagerank_sampled[input_page] += 1
        T_model = transition_model(corpus, input_page, damping_factor)
        # Select next_page by percentage
        prob_now = 0
        for page_linked in T_model:
            prob_now += T_model[page_linked]
            if prob <= prob_now:
                next_page = page_linked
                break
        input_page = next_page
        # Update sample count
        sample_count += 1
    for sample_page in corpus:
        pagerank_sampled[sample_page] = pagerank_sampled[sample_page]/n
    return pagerank_sampled

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_iterate = dict()
    pagerank_iterate_prev = dict()
    N = len(corpus)
    # Initial the two dict, with the pagerank_iterate prob set as 1/N
    for keys1 in corpus:
        pagerank_iterate_prev[keys1] = 0
        pagerank_iterate[keys1] = 1/N
    T = True
    # T=True while abs lower than 0.001
    while T:
        T = False
        for iterate_page in corpus:
            sum = 0
            for sub_page in corpus:
                # if the sub_page is empty, prob equals to the original prob + the prob of being at sub_page times 1/N
                if len(corpus[sub_page]) == 0:
                    sum += pagerank_iterate[sub_page]/N
                # Else, prob equals to the original prob + the prob of being at the sub_page and heading to the iterate_page
                else:
                    if iterate_page in corpus[sub_page]:
                        sum += pagerank_iterate[sub_page]/len(corpus[sub_page])
            pagerank_iterate_prev[iterate_page] = (1-damping_factor)/N + sum*damping_factor
        # if any absolute value of the prob diff > 0.001, T = True
        for key_2 in pagerank_iterate_prev:
            if abs(pagerank_iterate[key_2] - pagerank_iterate_prev[key_2]) > 0.001:
                T = True
            pagerank_iterate[key_2] = pagerank_iterate_prev[key_2]
    return pagerank_iterate




if __name__ == "__main__":
    main()
