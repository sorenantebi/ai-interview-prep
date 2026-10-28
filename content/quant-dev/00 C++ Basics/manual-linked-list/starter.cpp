#include <iostream>

struct Node {
    int value;
    Node* next;
};

Node* buildList(const int* values, int n) {
    // TODO: new a Node per value and append it at the tail
    return nullptr;
}

void printList(const Node* head) {
    // TODO: walk the list and print the values on one line
}

Node* reverseList(Node* head) {
    // TODO: iterate with prev / cur / next pointers
    return head;
}

int freeList(Node* head) {
    // TODO: delete every node (save next before deleting!) and count them
    return 0;
}

int main() {
    int n;
    std::cin >> n;
    // TODO: read the values, build, print, reverse, print, free, print "freed <count>"
    return 0;
}
