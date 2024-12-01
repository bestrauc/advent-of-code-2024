import utils
from collections import Counter

input = utils.read_puzzle_input("inputs/day1.txt")

list1, list2 = zip(*[utils.nums(line) for line in input])

# Part 1
sorted1 = sorted(list1)
sorted2 = sorted(list2)

sum = 0
for x, y in zip(sorted1, sorted2):
    sum += abs(x - y)

print(sum)

# Part 2
counts2 = Counter(list2)

similarity_score = 0
for x in list1:
    c = counts2[x]
    similarity_score += x * c

print(similarity_score)
