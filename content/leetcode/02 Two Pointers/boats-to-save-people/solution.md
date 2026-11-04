---
topic: "Two Pointers"
difficulty: Medium
leetcode: https://leetcode.com/problems/boats-to-save-people/
neetcode: https://neetcode.io/problems/boats-to-save-people
---
# Boats to Save People - Solution

## Intuition

The heaviest remaining person needs a boat no matter what. If the lightest remaining person can share that boat, pairing them is never worse, since the lightest person is the easiest to fit with anyone. If even the lightest cannot fit with the heaviest, the heaviest must travel alone.

## Approach

1. Sort `people` in ascending order.
2. Place pointer `left` at the lightest person and `right` at the heaviest.
3. While `left <= right`, the person at `right` takes a boat. If `people[left] + people[right] <= limit`, the person at `left` also boards and `left` moves forward.
4. Move `right` backward and count one boat.
5. Return the boat count.

## Code

```python
class Solution(object):
    def numRescueBoats(self, people: list[int], limit: int) -> int:
        people.sort()
        right = len(people) - 1
        left = res = 0
        while left <= right:
            if people[left] + people[right] <= limit:
                left += 1
            right -= 1
            res += 1
        return res
```

## Complexity

- **Time:** `O(n log n)` — dominated by sorting; the two-pointer sweep is `O(n)`.
- **Space:** `O(1)` — extra space aside from the sort (`O(n)` worst case depending on the sort implementation).

## Other Approaches

- **Counting sort + two pointers:** since weights are at most `limit`, bucket counts replace the comparison sort — Time `O(n + limit)` / Space `O(limit)`
- **Brute-force pairing:** for each person, search for the heaviest compatible unused partner — Time `O(n^2)` / Space `O(n)`

## C++

```cpp
/*
    Given an array of people's weight, people[i] is the weight of the ith person, 
    and there is an infinite number of boats where each boat can carry a maximum weight of limit. 
    Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most limit.
    Return minimum number of boats to carry every given person.

    sort, while there is people to carry 
    carry the heaviest and lightest person provided their weight doesn't exceed limit.
    otherwise, carry the heaviest person only

    Time: O(n)
    Space: O(1)
*/

class Solution {
public:
    int numRescueBoats(vector<int>& people, int limit) {
        sort(people.begin(), people.end());
        
        int boatRequired = 0;
        int lightestPerson = 0;
        int heaviestPerson = people.size()-1;

        //WHILE THERE IS SOMEONE TO CARRY
        while (lightestPerson <= heaviestPerson){
            if(people[lightestPerson] + people[heaviestPerson] <= limit){
                --heaviestPerson;
                ++lightestPerson;
            }
            else{
                --heaviestPerson;
            }
            ++boatRequired;
        }

        return boatRequired;
    }
};
```
