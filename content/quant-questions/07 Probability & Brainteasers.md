---
topic: "Probability & Brainteasers"
---
# Probability & Brainteasers

Classic quant interview puzzles; give the exact answer and a short derivation.

## Waiting for a Six · Easy

You roll a fair die until a 6 appears. What is the expected number of rolls?

### Answer

6. The number of rolls is geometric with success probability p = 1/6, and its mean is 1/p. Equivalently, E = 1 + (5/6)E gives E = 6.

## Two Sixes in a Row · Medium

You roll a fair die until you get two 6s in a row. What is the expected number of rolls?

### Answer

42. Let E be the expected rolls from scratch and F the expected rolls when the last roll was a 6. E = 1 + (1/6)F + (5/6)E and F = 1 + (1/6)·0 + (5/6)E. The first gives E = 6 + F; substituting, E = 6 + 1 + (5/6)E, so E/6 = 7 and E = 42.

## Seeing Every Face · Medium

How many rolls of a fair die do you expect to need before every face has appeared at least once?

### Answer

14.7. When k faces have been seen, a new face appears with probability (6−k)/6, so that stage takes 6/(6−k) rolls on average. Sum: 6(1/6 + 1/5 + 1/4 + 1/3 + 1/2 + 1) = 6 × 2.45 = 14.7.

## Ants on a Triangle · Easy

Three ants sit on the corners of a triangle. Each picks one of the two edges at random and walks along it at the same speed. What is the probability that no two ants collide?

### Answer

1/4. There are 2³ = 8 equally likely choices, and no collision happens only if all go clockwise or all go anticlockwise: 2/8. So a collision happens with probability 3/4. For an n-gon the no-collision probability is 2/2ⁿ.

## Poisoned Wine · Medium

One of 1000 bottles of wine is poisoned. Poison kills exactly 24 hours after drinking any amount. You have 24 hours and many test rats. What is the minimum number of rats needed to find the poisoned bottle?

### Answer

10. Number the bottles 0 to 999 in binary (10 bits, since 2¹⁰ = 1024 ≥ 1000). Rat i drinks from every bottle whose bit i is 1. After 24 hours the pattern of dead rats spells out the poisoned bottle's number in binary. Nine rats give only 512 distinct outcomes, which is not enough.

## Handshakes · Easy

At a party of n people, everyone shakes hands with everyone else exactly once. How many handshakes are there?

### Answer

n(n−1)/2. Each of the n people shakes n−1 hands, and that counts every handshake twice. It is the number of ways to choose 2 people from n, C(n, 2); for 30 people it is 435.

## Knockout Tournament · Easy

A single-elimination tennis tournament has 137 players, with byes where needed. How many matches are played?

### Answer

136. Every match eliminates exactly one player and every player except the champion is eliminated exactly once, so matches = players − 1. The bracket structure and byes do not matter.

## Gambler's Ruin Probability · Medium

You start with $30 and bet $1 on fair coin flips, stopping when you reach $100 or $0. What is the probability you reach $100? What if each flip is won with probability p ≠ 1/2?

### Answer

30/100 = 0.3. With a fair game your wealth is a martingale, so its expected final value equals the start: 100·P + 0·(1−P) = 30. In general, starting at i with target N: P = i/N for a fair game, and P = (1 − (q/p)ⁱ)/(1 − (q/p)ᴺ) with q = 1 − p otherwise.

## Expected Steps to Ruin · Medium

In the fair game above (start at $30, stop at $0 or $100), how many flips do you expect to make?

### Answer

30 × 70 = 2100. For a fair ±1 walk started at i with absorbing barriers 0 and N, the expected duration is i(N − i). It solves E(i) = 1 + ½E(i−1) + ½E(i+1) with E(0) = E(N) = 0, or follows from the martingale S² − t: E[S_T²] = 100² × 0.3 = 3000, so E[T] = 3000 − 30² = 2100.

## The Ballot Problem · Medium

In an election candidate A gets a votes and B gets b votes, with a > b. The votes are counted in random order. What is the probability that A is strictly ahead throughout the entire count?

### Answer

(a − b)/(a + b). By the reflection principle, the bad counting orders that start with a vote for A and later tie can be matched one-to-one with orders that start with a vote for B, and every order that starts with B is bad. So P(bad) = 2 × b/(a + b), giving 1 − 2b/(a + b) = (a − b)/(a + b). For 3 votes to 1: 1/2.

## First Ace · Medium

You shuffle a standard 52-card deck and turn cards over one at a time. What is the expected position of the first ace?

### Answer

53/5 = 10.6. The 4 aces split the 48 other cards into 5 gaps that by symmetry have equal expected size 48/5 = 9.6. The first ace comes after the first gap, so its expected position is 9.6 + 1 = 10.6. In general, with n cards and k special ones, it is (n + 1)/(k + 1).

## Birthday Problem · Easy

How many people do you need in a room for the chance that two share a birthday to exceed 50% (365 equally likely days, ignore leap years)?

### Answer

23. The chance that all n birthdays differ is (365/365)(364/365)…((365−n+1)/365). For n = 23 it is about 0.493, so a shared birthday has probability about 50.7%; for 22 it is about 47.6%. It is small because there are C(23, 2) = 253 pairs that could match.

## Monty Hall · Easy

There are three doors, one hiding a car. You pick a door; the host, who knows where the car is, always opens a different door showing a goat and offers you a switch. Should you switch, and what is your win probability?

### Answer

Switch: you win with probability 2/3. Your first pick is right with probability 1/3 and the host's action does not change that. In the other 2/3 of cases the car is behind one of the other two doors and the host has removed the goat, so switching wins exactly then.

## Two Children · Medium

A family has two children, and you are told at least one of them is a boy. What is the probability that both are boys? How does it change if you are told the older child is a boy?

### Answer

1/3, and 1/2. The equally likely families are BB, BG, GB, GG; "at least one boy" leaves BB, BG, GB, of which one is BB. "The older is a boy" leaves BB and BG, so 1/2. The answer depends on exactly how the information was obtained.

## Maximum of Two Dice · Medium

You roll two fair dice. What is the expected value of the larger number?

### Answer

161/36 ≈ 4.47. P(max ≤ k) = (k/6)², so P(max = k) = (k² − (k−1)²)/36 = (2k − 1)/36. Then E = Σ k(2k − 1)/36 = (1 + 6 + 15 + 28 + 45 + 66)/36 = 161/36.

## Broken Stick Triangle · Medium

A stick is broken at two points chosen independently and uniformly along its length. What is the probability the three pieces can form a triangle?

### Answer

1/4. The pieces form a triangle exactly when every piece is shorter than half the stick. With break points x and y in the unit square, each condition "piece ≥ 1/2" cuts out a triangle of area 1/4 (the three are disjoint), so the valid area is 1 − 3/4 = 1/4.

## Drunk on a Number Line · Medium

A drunk starts at 0 on the integer line and steps left or right with probability 1/2 each. What is the probability he ever returns to 0? What is the expected time until he does?

### Answer

He returns with probability 1, but the expected return time is infinite. The 1D simple random walk is recurrent: the expected number of visits to 0, Σ C(2n, n)/4ⁿ, diverges because the terms behave like 1/√(πn). The probability the first return takes longer than 2n also decays like 1/√n, whose sum diverges, so the mean is infinite. (In 2D it also returns surely; in 3D only with probability ≈ 0.34.)

## Bertrand's Box · Easy

Three boxes contain two gold coins, two silver coins, and one of each. You pick a box at random and draw a coin at random from it; it is gold. What is the probability the other coin in that box is gold?

### Answer

2/3. There are three equally likely gold coins you could have drawn; two of them are in the gold-gold box, where the other coin is gold, and one is in the mixed box. Answering 1/2 wrongly treats the two remaining boxes as equally likely.

## HH vs HT · Medium

You flip a fair coin repeatedly. What is the expected number of flips until you first see HH? Until you first see HT? Why are they different?

### Answer

HH takes 6, HT takes 4. For HT: wait for an H (2 flips on average), then wait for a T (2 more), since another H does not lose progress: 4. For HH: from scratch E = 1 + ½A + ½E, and after one H, A = 1 + ½·0 + ½E; solving gives E = 6. HH is slower because a failure after an H (getting T) sends you all the way back to the start, while for HT a failure (getting H) leaves you exactly where you were.

## St Petersburg Paradox · Medium

A fair coin is flipped until the first head. If the head comes on flip k you win 2ᵏ dollars. What is the fair price of this game, and why does nobody pay much for it?

### Answer

The expected payoff is infinite: Σ (1/2)ᵏ · 2ᵏ = 1 + 1 + 1 + … diverges. Yet people pay only a few dollars because the huge payoffs are extremely unlikely, utility of money is concave (with log utility the game is worth only a small finite amount), and in reality the payer's wealth is finite, which caps the payoff and makes the expected value just about log₂(bankroll).

## Die with One Re-roll · Medium

You roll a fair die and win its value in dollars. After seeing the first roll you may re-roll once and take the second result instead. What is the optimal strategy and the expected value? What if you may re-roll twice?

### Answer

Re-roll if you get 1, 2 or 3; the value is 17/4 = 4.25. A re-roll is worth 3.5, so keep 4, 5 or 6: E = (4 + 5 + 6)/6 + (3/6) × 3.5 = 2.5 + 1.75 = 4.25. With two re-rolls, the continuation after the first roll is worth 4.25, so keep only 5 or 6: E = (5 + 6)/6 + (4/6) × 4.25 = 14/3 ≈ 4.67.

## 100 Prisoners and Boxes · Hard

100 numbered prisoners, 100 boxes each containing a random distinct prisoner number. Each prisoner may open 50 boxes and all must find their own number, else everyone fails. They may agree a strategy beforehand but not communicate afterwards. What is the best known success probability?

### Answer

About 31.2%. Each prisoner opens the box with their own number, then the box numbered by what they find, and so on, following the cycle of the permutation that contains their number. Everyone succeeds exactly when the permutation has no cycle longer than 50. The probability of a cycle of length k > 50 is 1/k (at most one can exist), so P(success) = 1 − Σ_{k=51}^{100} 1/k ≈ 1 − 0.688 = 0.312, far better than (1/2)¹⁰⁰ for random guessing.

## Medical Test · Easy

A disease affects 1% of people. A test detects it 99% of the time when present and gives a false positive 5% of the time when absent. You test positive. What is the probability you have the disease?

### Answer

1/6 ≈ 16.7%. By Bayes: P(D | +) = (0.99 × 0.01) / (0.99 × 0.01 + 0.05 × 0.99) = 0.0099/0.0594 = 1/6. Out of 10,000 people, about 99 sick people test positive against about 495 healthy ones, so most positives are false because the disease is rare.

## Fixed Points of a Permutation · Medium

n people throw their hats in a pile and each takes one back at random. What is the expected number of people who get their own hat?

### Answer

1, for every n. Let Iₖ indicate that person k gets their own hat; P(Iₖ = 1) = 1/n. By linearity of expectation, which needs no independence, E = n × 1/n = 1. (The probability nobody gets their own hat tends to 1/e ≈ 0.368.)

## Trains and a Bird · Easy

Two trains are 120 km apart and head towards each other at 40 km/h and 20 km/h. A bird starts at the front of one train and flies back and forth between them at 90 km/h until they meet. How far does the bird fly?

### Answer

180 km. The trains close the gap at 60 km/h, so they meet after 120/60 = 2 hours, and the bird flies for 2 hours at 90 km/h. Summing the infinite series of individual legs gives the same answer but is unnecessary.
