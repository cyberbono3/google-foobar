"""
Doomsday Fule
Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state). You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
    [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
    [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
    [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
    [0,0,0,0,0,0],  # s3 is terminal
    [0,0,0,0,0,0],  # s4 is terminal
    [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:

s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that:

s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is [0, 3, 2, 9, 14].

Test Cases

Input:
    solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
    solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]

"""






import numpy as np
from fractions import Fraction
from fractions import gcd
from itertools import compress,starmap
from functools import reduce

def gcd1(L):

    return reduce(gcd, L)

def get_matrix_prob(M):

    M = np.asarray(M,dtype = float)
    states = []
    numr = 0
    for row in M:
        s = sum(a for a in row)
        if not s:
            row[numr] = 1
            states.append(True)
        else:
            states.append(False)
            nl = 0
            while nl < len(row):
                row[nl] = row[nl]/s
                nl += 1
        numr += 1
    return M,states


def get_vec(M):
    i = 0
    while i < 100:
	    M = np.linalg.matrix_power(M, 2)
	    i += 1
    return [float(v) for v in M[0]]

def compute_numerators_and_denominators(pv):
    nums, dens = [], []
    for i in pv:
        num = Fraction(i).limit_denominator().numerator 
        den = Fraction(i).limit_denominator().denominator
        nums.append(num)
        dens.append(den)
    return (nums, dens)

def compute_terminal_state_numerators(numerators, denominators, ts):
    j = 0
    td = list(denominators)
    tn = list(numerators)
    tm = list(numerators)

    while j < len(denominators):
        i = 0
        while i < len(denominators):
            if i != j:
                td[j] *= denominators[i] 
                tn[j] *= denominators[i] 
            i += 1
        tm[j] = Fraction(tn[j],td[j])
        j += 1
    den = gcd1(tm).denominator 
    j = 0
    while j < len(tn):
        td[j] /= den
        tn[j] /= td[j]
        j += 1
    tsnumerators = list(compress(tn, ts)) 
    return (den,tsnumerators)

def solution(m):
    if len(m) == 1:
        return [1, 1]
    pm,ts = get_matrix_prob(m) 

    pv = get_vec(pm) 

    numerators, denominators = compute_numerators_and_denominators(pv) 

    denominator,tsnumerators = compute_terminal_state_numerators(numerators, denominators, ts)

    res = list(tsnumerators) + [denominator]

    return list(map(int, res))
print(solution([
            [0, 2, 1, 0, 0],
            [0, 0, 0, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])==[7, 6, 8, 21])

print(solution([
            [0, 1, 0, 0, 0, 1],
            [4, 0, 0, 3, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])==[0, 3, 2, 9, 14])

print(solution([
            [0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])==[0, 1, 1, 3, 5])

print(solution([
            [1, 1, 0, 1],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])==[0, 1, 1])


print(solution([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ])==[1, 1])
print(solution([
            [0,0,0,1,0,1,0,0,0,2],
            [0,0,0,0,0,0,0,0,0,2],
            [0,0,0,0,0,0,0,0,2,2],
            [0,0,0,0,1,0,0,4,0,1],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,4,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,2],
            [0,0,0,0,0,0,0,0,2,0],
            [0,0,0,0,0,0,0,0,0,3],
            [0,0,0,0,0,0,0,0,0,0]])==[1, 11, 12])

print(solution([
            [0,10,0,0,1,0,0,1,0,0],
            [0,0,1,0,10,0,0,1,0,0],
            [1,0,0,11,0,2,10,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,3,0,0,0,0,0,0,4],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]])==[385, 9072, 350, 1782, 0, 40, 11629])

print(solution([[0,10,0,0,1,0,0,1,0,0],
            [0,0,1,0,10,0,0,1,0,0],
            [1,0,0,11,0,2,10,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,3,0,0,0,0,0,0,4],
            [666,0,0,0,1310,0,276,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]))
     # ==[151157138508775620608L, 3652912255657602187264L, 699641612519462535168L, 0, 15704637671688114176L, 4519415644450798732130L])
















