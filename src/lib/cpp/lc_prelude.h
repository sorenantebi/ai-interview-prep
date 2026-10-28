// What LeetCode's C++ environment gives you: the common headers, `using namespace std`, ListNode and TreeNode.
// Plus a small JSON reader/writer the bridge (lc_bridge.py) uses to call your Solution from the Python tests.
#pragma once
#include <algorithm>
#include <array>
#include <bitset>
#include <climits>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <deque>
#include <functional>
#include <iostream>
#include <limits>
#include <list>
#include <map>
#include <numeric>
#include <optional>
#include <queue>
#include <random>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;

#ifndef LC_OWN_LISTNODE
struct ListNode {
    int val;
    ListNode* next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};
#endif
#ifndef LC_OWN_TREENODE
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* left, TreeNode* right) : val(x), left(left), right(right) {}
};
#endif

namespace lc {
struct J {
    enum Kind { Null, Bool, Num, Str, Arr, Obj } kind = Null;
    bool b = false;
    double num = 0;
    long long i = 0;
    string s;
    vector<J> a;
    vector<pair<string, J>> o;
    const J* get(const string& k) const {
        for (auto& [key, v] : o) if (key == k) return &v;
        return nullptr;
    }
};

inline void ws(const string& t, size_t& p) { while (p < t.size() && isspace((unsigned char)t[p])) ++p; }
inline string str(const string& t, size_t& p) {
    string out;
    ++p;  // opening quote
    while (p < t.size() && t[p] != '"') {
        char c = t[p++];
        if (c != '\\') { out += c; continue; }
        char e = t[p++];
        if (e == 'n') out += '\n'; else if (e == 't') out += '\t'; else if (e == 'r') out += '\r';
        else if (e == 'b') out += '\b'; else if (e == 'f') out += '\f';
        else if (e == 'u') {  // \uXXXX (and surrogate pairs) -> UTF-8 bytes, like a LeetCode C++ string holds
            unsigned cp = stoul(t.substr(p, 4), nullptr, 16);
            p += 4;
            if (cp >= 0xD800 && cp < 0xDC00 && t.compare(p, 2, "\\u") == 0) {
                cp = 0x10000 + ((cp - 0xD800) << 10) + (stoul(t.substr(p + 2, 4), nullptr, 16) - 0xDC00);
                p += 6;
            }
            if (cp < 0x80) out += (char)cp;
            else if (cp < 0x800) { out += (char)(0xC0 | cp >> 6); out += (char)(0x80 | (cp & 0x3F)); }
            else if (cp < 0x10000) { out += (char)(0xE0 | cp >> 12); out += (char)(0x80 | (cp >> 6 & 0x3F)); out += (char)(0x80 | (cp & 0x3F)); }
            else { out += (char)(0xF0 | cp >> 18); out += (char)(0x80 | (cp >> 12 & 0x3F)); out += (char)(0x80 | (cp >> 6 & 0x3F)); out += (char)(0x80 | (cp & 0x3F)); }
        }
        else out += e;
    }
    ++p;
    return out;
}
inline J parse(const string& t, size_t& p) {
    ws(t, p);
    J j;
    char c = t[p];
    if (c == '[') {
        j.kind = J::Arr; ++p; ws(t, p);
        if (t[p] == ']') { ++p; return j; }
        while (true) { j.a.push_back(parse(t, p)); ws(t, p); if (t[p++] == ']') break; }
    } else if (c == '{') {
        j.kind = J::Obj; ++p; ws(t, p);
        if (t[p] == '}') { ++p; return j; }
        while (true) { ws(t, p); string k = str(t, p); ws(t, p); ++p; j.o.push_back({k, parse(t, p)}); ws(t, p); if (t[p++] == '}') break; }
    } else if (c == '"') { j.kind = J::Str; j.s = str(t, p); }
    else if (t.compare(p, 4, "null") == 0) { p += 4; }
    else if (t.compare(p, 4, "true") == 0) { j.kind = J::Bool; j.b = true; p += 4; }
    else if (t.compare(p, 5, "false") == 0) { j.kind = J::Bool; p += 5; }
    else {
        size_t start = p;
        while (p < t.size() && (isdigit((unsigned char)t[p]) || strchr("+-.eE", t[p]))) ++p;
        string n = t.substr(start, p - start);
        j.kind = J::Num; j.num = stod(n);
        j.i = n.find_first_of(".eE") == string::npos ? stoll(n) : (long long)j.num;
    }
    return j;
}

inline void quote(const string& s, string& out) {
    out += '"';
    for (char c : s) {
        if (c == '"' || c == '\\') { out += '\\'; out += c; }
        else if (c == '\n') out += "\\n";
        else if ((unsigned char)c < 0x20 || c == 0x7F) { char b[8]; snprintf(b, sizeof b, "\\u%04x", c); out += b; }
        else out += c;
    }
    out += '"';
}

// Conv<T>::in builds a T from JSON; Conv<T>::out writes a T as JSON.
template <class T, class = void> struct Conv;
template <class T> struct Conv<T, enable_if_t<is_integral_v<T> && !is_same_v<T, bool> && !is_same_v<T, char>>> {
    static T in(const J& j) { return j.kind == J::Bool ? (T)j.b : (T)j.i; }
    static void out(T v, string& o) { o += to_string(v); }
};
template <class T> struct Conv<T, enable_if_t<is_floating_point_v<T>>> {
    static T in(const J& j) { return (T)j.num; }
    static void out(T v, string& o) {
        if (!isfinite(v)) { o += "null"; return; }
        char b[64]; snprintf(b, sizeof b, "%.17g", (double)v); o += b;
    }
};
template <> struct Conv<bool> {
    static bool in(const J& j) { return j.kind == J::Bool ? j.b : j.i != 0; }
    static void out(bool v, string& o) { o += v ? "true" : "false"; }
};
template <> struct Conv<char> {
    static char in(const J& j) { return j.kind == J::Str ? (j.s.empty() ? '\0' : j.s[0]) : (char)j.i; }
    static void out(char v, string& o) { quote(string(1, v), o); }
};
template <> struct Conv<string> {
    static string in(const J& j) { return j.s; }
    static void out(const string& v, string& o) { quote(v, o); }
};
template <class T> struct Conv<vector<T>> {
    static vector<T> in(const J& j) {
        vector<T> v;
        v.reserve(j.a.size());
        for (auto& x : j.a) v.push_back(Conv<T>::in(x));
        return v;
    }
    static void out(const vector<T>& v, string& o) {
        o += '[';
        for (size_t k = 0; k < v.size(); ++k) { if (k) o += ','; Conv<T>::out(v[k], o); }
        o += ']';
    }
};
template <class A, class B> struct Conv<pair<A, B>> {
    static pair<A, B> in(const J& j) { return {Conv<A>::in(j.a[0]), Conv<B>::in(j.a[1])}; }
    static void out(const pair<A, B>& v, string& o) { o += '['; Conv<A>::out(v.first, o); o += ','; Conv<B>::out(v.second, o); o += ']'; }
};
// Which argument / position each input list node came from, so a returned list can reuse the caller's nodes
// (tests for e.g. Reverse Nodes in k-Group check the nodes themselves were relinked, not copied).
inline int cur_arg = 0, cur_index = 0;  // node position counts across a whole argument (vector<ListNode*> too)
inline unordered_map<const ListNode*, pair<int, int>> origin;

// A linked list is [values] or {"vals": [...], "pos": i} when the tail links back to node i (Linked List Cycle).
// It's written as [values], or {"vals": [...], "ids": [[arg, index] or null, ...]} when it reuses input nodes.
template <> struct Conv<ListNode*> {
    static ListNode* in(const J& j) {
        const J& vals = j.kind == J::Obj ? *j.get("vals") : j;
        long long pos = j.kind == J::Obj ? j.get("pos")->i : -1;
        ListNode dummy, *tail = &dummy;
        vector<ListNode*> nodes;
        for (auto& x : vals.a) {
            tail = tail->next = new ListNode((int)x.i);
            origin[tail] = {cur_arg, cur_index++};
            nodes.push_back(tail);
        }
        if (pos >= 0 && pos < (long long)nodes.size()) tail->next = nodes[pos];
        return dummy.next;
    }
    static void out(ListNode* h, string& o) {
        string vals = "[", ids = "[";
        bool reused = false;
        for (int n = 0; h && n < 1000000; h = h->next, ++n) {
            if (n) { vals += ','; ids += ','; }
            vals += to_string(h->val);
            auto it = origin.find(h);
            if (it == origin.end()) ids += "null";
            else { reused = true; ids += "[" + to_string(it->second.first) + "," + to_string(it->second.second) + "]"; }
        }
        if (reused) o += "{\"vals\":" + vals + "],\"ids\":" + ids + "]}";
        else o += vals + ']';
    }
};
// A tree is its level-order list with nulls, like LeetCode prints it.
template <> struct Conv<TreeNode*> {
    static TreeNode* in(const J& j) {
        if (j.a.empty() || j.a[0].kind == J::Null) return nullptr;
        TreeNode* root = new TreeNode((int)j.a[0].i);
        deque<TreeNode*> q{root};
        size_t k = 1;
        while (!q.empty() && k < j.a.size()) {
            TreeNode* n = q.front(); q.pop_front();
            if (k < j.a.size() && j.a[k].kind != J::Null) q.push_back(n->left = new TreeNode((int)j.a[k].i));
            ++k;
            if (k < j.a.size() && j.a[k].kind != J::Null) q.push_back(n->right = new TreeNode((int)j.a[k].i));
            ++k;
        }
        return root;
    }
    static void out(TreeNode* root, string& o) {
        vector<TreeNode*> order{root};
        for (size_t k = 0; k < order.size(); ++k) if (order[k]) { order.push_back(order[k]->left); order.push_back(order[k]->right); }
        while (!order.empty() && !order.back()) order.pop_back();
        o += '[';
        for (size_t k = 0; k < order.size(); ++k) { if (k) o += ','; o += order[k] ? to_string(order[k]->val) : "null"; }
        o += ']';
    }
};

// For arguments that are nodes inside an earlier tree argument (e.g. p and q in Lowest Common Ancestor).
inline TreeNode* find(TreeNode* root, int val) {
    vector<TreeNode*> st{root};
    while (!st.empty()) {
        TreeNode* n = st.back(); st.pop_back();
        if (!n) continue;
        if (n->val == val) return n;
        st.push_back(n->left); st.push_back(n->right);
    }
    return new TreeNode(val);
}
template <class T> T arg(const J& j, TreeNode* tree) {
    if constexpr (is_same_v<T, TreeNode*>) {
        if (tree && j.kind == J::Obj && j.get("node")) return find(tree, (int)j.get("node")->i);
    }
    return Conv<T>::in(j);
}
template <class T> string json(const T& v) { string o; Conv<T>::out(v, o); return o; }
}  // namespace lc
