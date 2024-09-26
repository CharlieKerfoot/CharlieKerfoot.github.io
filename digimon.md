---
layout: page
title: Digimon Project
subtitle: Tracking Digimon Stats From a CSV
comments: true
---

### The ["Digimon Database"](https://www.kaggle.com/datasets/rtatman/digidb) dataset on Kaggle contains many different stats and attributes about a plethora of Digimon (digital monsters).

Each Digimon has an id, name, stage, type, attribute, etc.
Here are the first five entries in the dataset:

|Number|Digimon|Stage|Type|Attribute|Memory|Equip Slots|HP|SP|Atk|Def|Int|Spd|
|:----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:------:|:-----:|:------:
|1     |Kuramon|Baby|Free|Neutral|2|0|590|77|79|69|68|95|
|2     |Pabumon|Baby|Free|Neutral|2|0|950|62|76|76|69|68|
|3     |Punimon|Baby|Free|Neutral|2|0|870|50|97|87|50|75|
|4     |Botamon|Baby|Free|Neutral|2|0|690|68|77|95|76|61|
|5     |Poyomon|Baby|Free|Neutral|2|0|540|98|54|59|95|86|

The first question I had to answer was:

## 1. What is the average HP of all the Digimon?

In my mind, there were two main ways to solve this problem: 

### A quick, potentially one-line solution that just printed out the answer

`def find_avg(file, parameter):
    with open(file, "r") as f:
        data = list(csv.DictReader(f))
        print(sum(float(row[parameter]) for row in data)/len(data))`

I simply used the [built-in sum function](https://docs.python.org/3/library/functions.html#sum) to get the total HP of all the digimon and then divides it by the number of digimon (using the length of the dataset). I like how this function is so concise and only uses one line but it can be hard to read and the output is basically just a magic number outside of the context of the question. 

### A less efficient and longer solution that used a nested dictionary to more cleanly display the data and could be use more dynamically

`def find_avg(file, parameter):
    answers = defaultdict(lambda: {"total": 0, "count": 0})

    with open(file, "r) as f:
        for row in data:

            answers[row[parameter]]["total"] += value
            answers[row[parameter]]["count"] += 1
            answers[row[parameter]]["average"] = answers[row[parameter]]["total"] / answers[row[parameter]]["count"]

    print(dict(answers))`

Here, I, instead, set up a nested dictionary which holds the values of `[total]`, `[count]`, and `[average]` and then returns the whole dictionary rather than just the average HP value. While this function is clearly more verbose and uses more lines of code, the code itself is far more readable and the output allows the user to see the count and total aside from just the average. For a straightforward problem like this one, I might prefer the first solution but the organization of a nested dictionary data structure is much more convenient as the problem scales in complexity.

Calling find_avg("datasets/digimon.csv", "HP") on both functions will return the same, correct answer. It just comes down to what you are prioritizing and what style your prefer when answering the question. 

## 2. Write a function that can count the number of Digimon with a specific attribute. 

The key difference in this question is the generalization of the parameters, where an answer for the first question could have only accepted the `"HP"` variable while this question requires the ability to accept any variable or stat. I think this is a good practice in general, though, to write more dynamic code, so both of my first solutions could already take in any stat. Again, in a similar fashion to the previous question, two possible solutions immediately spawn in my mind.  I have already outlined the pros and cons of both methods so here are simply the two functions:

### One-Liner Solution

`def count_digimon(file, category, value):
    with open(file, "r") as f:
        data = csv.DictReader(f)
        print(sum(1 for row in data if row[category] == value))`

This function is almost identical to the first solution of the previous problem. All that is changed is the lack of division over the count and the addition of the condition which adds one to the count if the condition is met.

### Nested Dictionary Solution

`def find_avg(file, category, value):
    answers = defaultdict(lambda: {"count": 0})

    with open(file, "r) as f:
        for row in data:
            if row[category] == value:
                answers[row[parameter]]["count"] += 1

    print(dict(answers))`

Compared to the last problem, I really don't like this solution that much. The question is asking for so little that the nested dictionary really just starts to take up extra space and becomes a nuisance rather than a convenient data structure and potential future-proofing infrastructure.

## 3. Name a team of up to 3 Digimon that has at least 300 attack (Atk) but doesn't exceed 15 memory.

Now this is the really where the fun begins. While the previous two questions may have taken some thinking to write the code or come up with a better solution, ultimately they were pretty trivial and most people would have at least some idea of where to start when approached with those problems. Question three, however, is not like that.

Immediately, upon reading the question, I thought of the 0/1 knapsack problem, a very common programming problem that requires a dynamic programming solution to achieve polynomial time response (not to be confused with the fractional knapsack problem which can simply be answered with a heuristic greedy algorithm). 

The problem goes as follows: 

### Given `N` items where each item has some `weight` and `profit` associated with it and also given a bag with capacity `W`, [i.e., the bag can hold at most `W` weight in it]. The task is to put the items into the bag such that the sum of profits associated with them is the maximum possible.

While the brute force solution (trying all possible subsets of the N items) can work, the method is quite slow with a O(2^n^). Instead, there is a faster method (O(N * W)) which involves making a table for every possible value W and every amount of items 0 through N.

Say the input is W = 4, profit[] = {1, 2, 3}, weight[] = {10, 15, 20}

|N/W|0|1|2|3|4|5|6|
|-|-|-|-|-|-|-|-|
|0|0|0|0|0|0|0|0|
|1|0|10|15|20|20|20|20|
|2|0|10|15|25|30|35|35|
|3|0|10|15|25|30|35|45|

The leftmost column represents N (or the number of items we can use) and the top row represents the weight capacity which increments until it reaches W.

When generating the table, each cell can be made by evaluating the new item which can be added and choosing one of two options. 
1. The item doesn't provide enough profit compared to its weight and adding it would exceed the weight capacity, so the value of the cell becomes the same as the one right above it (no item added) 
2. The item should be added so you have to make room for it within the weight capacity. Take the cell right above it and then move w unit(s) left (where w represents the weight of the new item). Add the profit of the new item and that is the value of the cell. 

The best possible profit within W is always stored in the bottom right corner of the table.

The implementation and probably a better solution can be [here](https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/).

If we extrapolate some of those ideas, we can create a table that represents our digimon problem in a similar manner.

{Digimon: Kuramon, Memory: 2, Atk: 79} \
{Digimon: Motimon, Memory: 3, Atk: 82} \
{Digimon: Agumon, Memory: 5, Atk: 131}

|N/M|0|1|2|3|4|5|6|7|
|-|-|-|-|-|-|-|-|-|
|0|0|0|0|0|0|0|0|0|
|1|0|0|79|82|82|131|131|131|
|2|0|0|79|82|82|161|161|210|
|3|0|0|79|82|82|161|161|210|

This idea works mostly, BUT the original question contains two extra constraints that aren't included in this tabulation solution. 

Firstly, we cannot formulate a team with more than 3 digimon. Intuitively, and based on the difference in time complexity O(n^3^) vs O(2^n^), you might think that this constraint makes the code simpler rather than more verbose. But, the original dp solution can include as many digimon as possible, as long as the total team weight doesn't exceed the capacity, so we have to do extra work to adapt a classic dp solution to this problem. 

The second key difference is that the question requires outputting the team of digimon, rather than just the total attack value. This requires a lot of extra code and space to track which digimon were selected (instead of just what attack values they contributed).

With all these things in mind, here is my implementation and solution to the problem:

```python def find_max_atk(file, max_digi, max_mem):
    with open(file, "r") as f:
        data = list(csv.DictReader(f))
        
        dp = [[0] * (max_digi + 1) for _ in range(max_mem + 1)]
        selected = [[[-1] * (max_digi + 1) for _ in range(max_mem + 1)] for _ in range(len(data) + 1)]

        for i, row in enumerate(data):
            for j in range(max_mem, int(row["Memory"]) - 1, -1):
                for k in range(max_digi, 0, -1):
                    new_atk = dp[j - int(row["Memory"])][k - 1] + int(row["Atk"])

                    if new_atk > dp[j][k]:
                        dp[j][k] = new_atk
                        selected[i % 2][j][k] = i 

        max_attack_value = dp[max_mem][max_digi]

        team = []
        while max_digi > 0:
            digimon_index = selected[len(data) % 2][max_mem][max_digi] 
            if digimon_index == -1:
                break

            digimon = data[digimon_index]
            team.append(digimon['Digimon'])
            max_mem -= int(digimon['Memory'])
            max_digi -= 1

        return max_attack_value, team
```

I created to multi-dimensional arrays to track both the max attack of the team and the Digimon selected in this team. The for loop is pretty much the same implementation as the dynamic programming solution with one extra loop to account for the `max_digi` constraint. 

The final bit of the code directly addresses our second issue. After finding the team with the most attack (that didn't exceed the `max_mem`) and then backtracks through the selected list to find the digimon that made up that team.

## Conclusion





