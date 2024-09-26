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

This function simply uses the [built-in sum function](https://docs.python.org/3/library/functions.html#sum) to get the total HP of all the digimon and then divides it by the number of digimon (using the length of the dataset). I like how this function is so concise and only uses one line but it can be hard to read and the output is basically just a magic number outside of the context of the question. 

### A less efficient and longer solution that used a nested dictionary to more cleanly display the data and could be use more dynamically

`def find_avg(file, parameter):
    answers = defaultdict(lambda: {"total": 0, "count": 0})

    with open(file, "r) as f:
        for row in data:

            answers[row[parameter]]["total"] += value
            answers[row[parameter]]["count"] += 1
            answers[row[parameter]]["average"] = answers[row[parameter]]["total"] / answers[row[parameter]]["count"]

    print(dict(answers))`

In this function, I, instead, set up a nested dictionary which holds the values of `[total]`, `[count]`, and `[average]` and then returns the whole dictionary rather than just the average HP value. While this code is clearly more verbose and uses more lines of code, the code itself is far more readable and the output allows the user to see the count and total aside from just the average. For a straightforward problem like this one, I might prefer the first solution but the organization of a nested dictionary data structure is much more convenient as the problem scales in complexity.

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

Compared to the last problem, I really don't like this solution that much. The question is asking for so little that the nested dictionary really just starts to take up extra space and becomes a nuisance more than a convenient data structure, serving as infrastructure.

## 3. Name a team of up to 3 Digimon that has at least 300 attack (Atk) but doesn't exceed 15 memory.



