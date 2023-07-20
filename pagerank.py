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

    # Initialize a probability distribution dictionary
    prob_distribution = dict()
    for p in list(corpus.keys()):
        prob_distribution[p] = 0

    # Choose a link at random linked to by `page`
    if random.random() < damping_factor:
        # List links that are linked by `page`
        linked_pages = list(corpus[page])
        distribution = damping_factor / len(linked_pages)
        additional = (1 - damping_factor) / (len(linked_pages) + 1)
        # Set probability distribution
        for link in linked_pages:
            prob_distribution[link] = distribution + additional
        prob_distribution[page] = additional
        return prob_distribution
    else: # Choose a link at random chosen from all pages
        # List links of all page
        all_links = list(corpus.keys())
        distribution = 1 / len(all_links)
        # Set probability distribution
        for link in all_links:
            prob_distribution[link] = distribution
        return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Turn links into list for easier itteration
    links = list(corpus.keys())

    # Choose the first random page
    random_page = random.choice(links)

    # Initialize a pagerank dictionary
    s_pagerank = dict()
    for p0 in links:
        s_pagerank[p0] = 0

    # Add 1 to first random page visited
    s_pagerank[random_page] += 1

    for _ in range(n):
        # Get probability distribution
        probability = transition_model(corpus, random_page, damping_factor)
        # Randomly choose a page from the distribution
        random_page = random.choices(list(probability.keys()), list(probability.values()), k=1)[0]
        # Add 1 to randomly chosen page
        s_pagerank[random_page] += 1
    
    # Turn number of visits into percentage
    for p1 in links:
        s_pagerank[p1] /= n

    return s_pagerank 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize convergence threshold +/-0.001
    convergence_threshold = 0.0005

    # Initialize a pagerank dictionary
    initial_pagerank = dict()
    links = list(corpus.keys())
    for p0 in links:
        initial_pagerank[p0] = 1 / len(links)

    # Repeat while convergence threshold is not met
    while True:
        # Initialize a new dictionary
        new_pagerank = dict()

        # Iterate through every page
        for p1 in links:
            # Pagerank algorithm
            calculated_pagerank = (1 - damping_factor) / len(links)
            for other_page in links:
                # Check if current page is linked by other pages
                if p1 in corpus[other_page]:
                    calculated_pagerank += damping_factor * (initial_pagerank[other_page] / len(corpus[other_page]))
            
            # Set current page's pagerank
            new_pagerank[p1] = calculated_pagerank

        # Calculate change between current and new pagerank
        change = abs(new_pagerank[links[0]] - initial_pagerank[links[0]])

        # Break out of while loop if convergence threshold is met
        if change < convergence_threshold:
            break
        
        initial_pagerank = new_pagerank

    return initial_pagerank


if __name__ == "__main__":
    main()
