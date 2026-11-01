# Week 2 write-up: Dynamic Programming

## 1. 0/1 knapsack

### Hand-traced example: 0/1 knapsack

**The problem.** A truck can carry 7 kg. Each item can be taken whole or left behind.

| Item | Weight (kg) | Value |
|------|-------------|-------|
| A    | 1           | 1     |
| B    | 3           | 4     |
| C    | 4           | 5     |
| D    | 5           | 7     |

For each new item there are only two choices,

1. Skip it - The value is the same as the cell directly above.
2. Take it - The value is the item's value plus the best value for the remaining space, found in the row above at `c - weight`.


| Items allowed ↓ / Truck capacity → | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|------------------------------------|---|---|---|---|---|---|---|---|
| none                               | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A                                  | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| A, B                               | 0 | 1 | 1 | 4 | 5 | 5 | 5 | 5 |
| A, B, C                            | 0 | 1 | 1 | 4 | 5 | 6 | 6 | 9 |
| A, B, C, D                         | 0 | 1 | 1 | 4 | 5 | 7 | 8 | 9 |

The answer is : 9


Which items are choosen,

Start at the bottomright cell and move up. If the value is different from the cell above, that item was taken, so subtract its weight from the capacity.

| Row | Value here | Value above | Taken? | Capacity left |
|-----|------------|-------------|--------|---------------|
| D   | 9          | 9           | No     | 7             |
| C   | 9          | 5           | Yes    | 7 - 4 = 3     |
| B   | 4          | 1           | Yes    | 3 - 3 = 0     |
| A   | 0          | 0           | No     | 0             |

Result: take B and C since its Weight is 7 kg and value is 9.