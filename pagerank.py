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
    distribution = {}
    pages = set(corpus.keys())
    n = len(pages)

    links = corpus[page]

    # If page has no outgoing links, treat it as linking to all pages
    if len(links) == 0:
        for p in pages:
            distribution[p] = 1 / n
        return distribution

    # Base probability for all pages
    for p in pages:
        distribution[p] = (1 - damping_factor) / n

    # Add damping factor probability to linked pages
    for linked_page in links:
        distribution[linked_page] += damping_factor / len(links)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling.
    """

    pagerank = {page: 0 for page in corpus}
    pages = list(corpus.keys())

    # First sample: choose a page at random
    current_page = random.choice(pages)
    pagerank[current_page] += 1

    # Remaining samples
    for _ in range(1, n):
        distribution = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            population=list(distribution.keys()),
            weights=list(distribution.values()),
            k=1
        )[0]
        pagerank[current_page] += 1

    # Normalize counts to probabilities
    for page in pagerank:
        pagerank[page] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteration.
    """
    n = len(corpus)
    pagerank = {page: 1 / n for page in corpus}

    while True:
        new_pagerank = {}
        max_change = 0

        for page in corpus:
            total = 0
            for possible_page in corpus:
                links = corpus[possible_page]
                if len(links) == 0:
                    total += pagerank[possible_page] / n
                elif page in links:
                    total += pagerank[possible_page] / len(links)

            new_pagerank[page] = (1 - damping_factor) / n + damping_factor * total
            max_change = max(max_change, abs(new_pagerank[page] - pagerank[page]))

        pagerank = new_pagerank

        if max_change < 0.001:
            break

    return pagerank


if __name__ == "__main__":
    main()
