# SmartCity Logistics

This is a command line toolkit for a delivery company. It solves seven logistics problems with
three algorithm paradigms: Divide & Conquer, Greedy and Dynamic Programming, and all are connected to one dashboard using (`main.py`).

## Requirements 

- Python 3.8 or newer and standard library only.
- Open a terminal inside the project folder first.

## Run The program and Tests
1. To Run the main program with interactive menu,
        - python main.py  

2. To Run one feature only,
        - python main.py [num] # feature num in dashboard

3. To Run unit all unit tests,
        - python -m unittest discover -s tests -t .       # output is OK if all tests passing

4. To Run Test files one by one,
        - python -m unittest tests.test_merge_sort -v
        - python -m unittest tests.test_closest_pair -v
        - python -m unittest tests.test_greedy -v
        - python -m unittest tests.test_huffman -v
        - python -m unittest tests.test_knapsack -v
        - python -m unittest tests.test_dp -v
        - python -m unittest tests.test_shortest_path -v


## Week 01 Divide & Conquer - Day 1-3 Deliverable

1. **Merge sort comparisons vs n log₂ n**

| n     | Comparisons | n*log₂ n | Ratio |
|-------|-------------|----------|-------|
| 100   | 557         | 664      | 0.838 |
| 1000  | 8710        | 9966     | 0.874 |
| 10000 | 120351      | 132877   | 0.906 |

2. **Closest pair, brute force vs divide & conquer** 

| n    | Brute force (s) | Divide & conquer (s) |
|------|-----------------|----------------------|
| 100  | 0.00124         | 0.00099              |
| 1000 | 0.12139         | 0.000598             |



## Week 01  Greedy - Day 4-7 Deliverable

1. **Activity selection** 

We always pick the delivery that finishes first, because it provides the most time for the other deliveries. Lets say someone gives us the best possible schedule, and its first delivery is not the one that finishes first then We can swap that delivery for the one that finishes first, and nothing will clash, because the new one ends earlier. The schedule still has the same number of deliveries, so it is still a best schedule. We repeat this for every pick, so the greedy schedule is just as good as the best one.

2. **Why greedy fails for 0/1 knapsack** 

lets say Capacity is 50 kg and items weight and value as  A = (10, 60), B = (20, 100) and C = (30, 120). 

Greedy picks the items with the best value for their weight so it takes A and B and that leaves 20 kg of space left but C weighs 30 kg and doesn’t fit in since capacity is 50kg so the space is wasted. If we skips A and takes B and C then it fill the whole truck. If the items could be cut then greedy would fill the leftover space with part of C, so it works only when items can be divided.


3. **Huffman compression of `sample_manifest.txt`** 

| Original (bits) | Compressed (bits) | Ratio | Saved |
|-----------------|-------------------|-------|-------|
| 8832            | 5028              | 1.76x | 43.1% |


## Week 02 Dynamic Programming - Day 8-12 Deliverable

1. **0/1 knapsack: DP Table** - WRITEUP.md

## Week 02 Integration - Days 13–14 Deliverables 

Features and paradigms

| # | Feature                  |           What it does                                       |      Module                               | Paradigm              |
|---|--------------------------|--------------------------------------------------------------|-------------------------------------------|-----------------------|
| 1 | Sort packages            | Sorts the warehouse queue by deadline and counts comparisons | `divide_conquer/merge_sort.py`            | Divide & Conquer      |
| 2 | Closest hubs             | Finds the two nearest hubs, compares with brute force        | `divide_conquer/closest_pair.py`          | Divide & Conquer      |
| 3 | Schedule deliveries      | Most non overlapping deliveries for one driver               | `greedy/activity_selection.py`            | Greedy                |
| 4 | Load van (divisible)     | Fills the van by best value per kg, splitting the last item  | `greedy/fractional_knapsack.py`           | Greedy                |
| 5 | Compress manifest        | Huffman encodes and decodes the manifest, reports the ratio  | `greedy/huffman.py`                       | Greedy                |
| 6 | Load truck (indivisible) | Exact 0/1 knapsack with 2D and 1D tables                     | `dynamic_programming/knapsack_01.py`      | Dynamic Programming   |
| 7 | Cheapest route           | Cheapest path through the road graph                         | `dynamic_programming/shortest_path_dp.py` | Dynamic Programming   |


Complexity summary

n = items or points, W = knapsack capacity, k = distinct characters, V/E = graph nodes/edges.

| Algorithm               | Time           | Extra space |
|-------------------------|----------------|-------------|
| Merge sort              | O(n log n)     | O(n)        | 
| Closest pair            | O(n log n)     | O(n)        | 
| Activity selection      | O(n log n)     | O(n)        | 
| Fractional knapsack     | O(n log n)     | O(n)        | 
| Huffman coding          | O(n + k log k) | O(k)        |
| 0/1 knapsack, 2D table  | O(nW)          | O(nW)       | 
| 0/1 knapsack, 1D array  | O(nW)          | O(W)        | 
| Bellman-Ford            | O(VE)          | O(V)        | 


Why each paradigm fits

**Divide & Conquer: merge sort and closest pair**

These problems are easy to cut in half. Sorting packages is just sorting two lists
and joining them. Finding the closest hubs is also the same which find the closest pair on the left,
find it on the right, then check only the pairs that cross the middle. The two halves don't
depend on each other, and joining the answers is cheap, so splitting makes the work much smaller.

**Greedy: activity selection, fractional knapsack and Huffman**

In these problems, the best choice right now is also part of the best final answer, so we never
need to go back and change a choice.

- Activity selection: the job that finishes first leaves the time for other jobs, so it is always safe to pick.
- Fractional knapsack: the item with the best value per kg is always worth loading first, and the leftover space can be filled with a piece of the next item.
- Huffman: the two rarest characters can always be joined first, because they should get the longest codes.

**Dynamic Programming: 0/1 knapsack and shortest path**

Here greedy goes wrong, because one early choice can block a better combination. For example, a
good item may leave a gap that nothing else fits. So we have to compare many combinations. The
problem repeats itself and the same questions come up again and again. A table lets us answer 
each small question once, write it down, and reuse it,instead of recalculating it every time.

- 0/1 knapsack: the table stores the best value for every number of items and every capacity.
- Shortest path: the cheapest route to a place is built from the cheapest routes to the places before it.