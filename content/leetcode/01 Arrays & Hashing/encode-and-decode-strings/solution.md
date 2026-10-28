---
topic: "Arrays & Hashing"
difficulty: Medium
leetcode: https://leetcode.com/problems/encode-and-decode-strings/
neetcode: https://neetcode.io/problems/string-encode-and-decode
---
# Encode and Decode Strings - Solution

**Question:** Encode and Decode Strings - Question · **Difficulty:** Medium

## Intuition

Any delimiter character could also appear inside a string, so we cannot just join on a separator. Instead, prefix each string with its length and a marker, e.g. `"5#hello"`. When decoding we read the digits up to the first `#`, then take exactly that many characters, so the content is never interpreted, no matter what it contains.

## Approach

1. **Encode:** for each string `w`, append `f"{len(w)}#{w}"`; join everything together.
2. **Decode:** start at `i = 0`. Scan forward from `i` to the next `#` at `j`; `length = int(s[i:j])`.
3. The string is `s[j + 1 : j + 1 + length]`; append it and set `i = j + 1 + length`.
4. Repeat until `i` reaches the end of `s`.

## Code

```python
class Solution:
    def encode(self, strs):
        res = []
        for s in strs:
            res.append(str(len(s)))
            res.append("#")
            res.append(s)
        return "".join(res)

    def decode(self, s):
        res = []
        i = 0
        
        while i < len(s):
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            i = j + 1
            j = i + length
            res.append(s[i:j])
            i = j
            
        return res
```

## Complexity

- **Time:** `O(N)` — `N` is the total number of characters across all strings; each is written and read a constant number of times.
- **Space:** `O(N)` — for the encoded string and decoded output (no extra beyond the outputs).

## Other Approaches

- **Escaping a delimiter:** double every `#` inside strings and separate items with `" # "`-style tokens — Time `O(N)`, Space `O(N)`, but fiddlier to get right.
- **Fixed-width length header:** write each length as a 4-byte / fixed-width field instead of `len#` — Time `O(N)`, Space `O(N)`.

## Key Takeaway

Length-prefix framing (`len#payload`) is the robust way to serialize arbitrary strings; it is exactly how many network protocols (and chunked encodings) frame messages.

## C++

```cpp
/*
    Design algorithm to encode/decode: list of strings <-> string

    Encode/decode w/ non-ASCII delimiter: {len of str, "#", str}

    Time: O(n)
    Space: O(1)
*/

class Codec {
public:

    // Encodes a list of strings to a single string.
    string encode(vector<string>& strs) {
        string result;
        
        for (const string& str : strs) {
            result.append(to_string(str.size()));
            result.push_back('#');
            result.append(str);
        }
        
        return result;
    }

    // Decodes a single string to a list of strings.
    vector<string> decode(string s) {
        vector<string> result;
        
        int i = 0;
        while (i < s.size()) {
            int j = i;
            while (s[j] != '#') {
                j++;
            }
            int length = stoi(s.substr(i, j - i));
            string str = s.substr(j + 1, length);
            result.push_back(str);
            i = j + 1 + length;
        }
        
        return result;
    }
private:
};

// Your Codec object will be instantiated and called as such:
// Codec codec;
// codec.decode(codec.encode(strs));
```
