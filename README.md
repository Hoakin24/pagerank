# PageRank Algorithm

This repository contains a Python implementation of the PageRank algorithm. PageRank is a method used to rank web pages in search engine results based on their importance and popularity. It was developed by Larry Page and Sergey Brin, the founders of Google, and is one of the key components of Google's search algorithm.

## How to Run

To run the PageRank algorithm, you will need to have Python installed on your system. Clone this repository and navigate to the project directory. Then, you can run the following command to see the results from sampling and iteration:

```
python pagerank.py corpus
```

The program will output the estimated PageRank values for each page based on sampling and iterative updating.

## Files

- `pagerank.py`: This is the main Python file that implements the PageRank algorithm using both sampling and iterative updating. It calculates the PageRank values for the web pages based on their links and connectivity.

## Dependencies

There are no external dependencies required to run this program.

## How the AI Works

The PageRank algorithm assigns a numerical value to each web page in a corpus, representing the importance of the page. The higher the PageRank value, the more important the page is considered to be. The algorithm works by analyzing the links between web pages in the corpus and calculating the probability that a random surfer (a hypothetical person browsing the web by clicking on links at random) would visit each page.

The program uses two approaches to calculate the PageRank values:

1. Sampling Approach: The program uses random sampling to estimate the PageRank values. It starts with a random page and then simulates the behavior of a random surfer by following links to other pages based on a probability distribution. The process is repeated for a large number of samples, and the program counts the number of times each page is visited. The estimated PageRank values are then calculated based on the number of visits.

2. Iterative Approach: The program uses an iterative algorithm to update the PageRank values until convergence. It starts by assigning an initial PageRank value of 1/N to each page, where N is the total number of pages. The algorithm then iteratively updates the PageRank values based on the links between pages. It calculates the PageRank for each page as a combination of the probability of following links and the probability of randomly jumping to any page. The process is repeated until the PageRank values converge (i.e., the change in values becomes small enough).

Both approaches should produce similar results, with the iterative approach being more accurate but potentially slower for larger corpora.
