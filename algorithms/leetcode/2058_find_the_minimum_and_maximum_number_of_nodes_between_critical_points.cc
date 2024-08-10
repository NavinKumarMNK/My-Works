#include <iostream>
#include <vector>
#include <climits> // For INT_MAX
using namespace std;

// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    vector<int> nodesBetweenCriticalPoints(ListNode* head) {
        vector<int> criticalPoints;
        ListNode *prev = nullptr;
        ListNode *curr = head;

        int position = 0;
        while (curr != nullptr && curr->next != nullptr) {
            if (prev != nullptr && curr->next != nullptr) {
                if ((curr->val > prev->val && curr->val > curr->next->val) || 
                    (curr->val < prev->val && curr->val < curr->next->val)) {
                    criticalPoints.push_back(position);
                }
            }
            prev = curr;
            curr = curr->next;
            position++;
        }

        if (criticalPoints.size() < 2) {
            return {-1, -1};
        }

        int minD = INT_MAX;
        int maxD = criticalPoints.back() - criticalPoints.front();

        for (int i = 1; i < criticalPoints.size(); i++) {
            minD = min(minD, criticalPoints[i] - criticalPoints[i - 1]);
        }

        return {minD, maxD};
    }
};

// Function to create a linked list from a vector of values
ListNode* createLinkedList(const vector<int>& values) {
    if (values.empty()) return nullptr;
    ListNode* head = new ListNode(values[0]);
    ListNode* current = head;
    for (size_t i = 1; i < values.size(); ++i) {
        current->next = new ListNode(values[i]);
        current = current->next;
    }
    return head;
}

// Function to run test cases
void runTestCase(const vector<int>& values, const vector<int>& expected) {
    ListNode* head = createLinkedList(values);
    Solution sol;
    vector<int> result = sol.nodesBetweenCriticalPoints(head);

    if (result == expected) {
        cout << "Test case passed" << endl;
    } else {
        cout << "Test case failed" << endl;
    }
}

int main() {
    // Test case 1
    vector<int> values2 = {5, 3, 1, 2, 5, 1, 2};
    vector<int> expected2 = {1, 3}; // Expected output
    runTestCase(values2, expected2);

    // Test case 2
    vector<int> values3 = {1, 2, 3, 4, 5};
    vector<int> expected3 = {-1, -1}; // Expected output
    runTestCase(values3, expected3);

    return 0;
}