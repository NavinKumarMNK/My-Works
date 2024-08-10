#include <iostream>
#include <vector>
#include <cassert>
using namespace std;

class Solution {
public:
    // O(n) solution
    int passThePillow(int n, int time) {
        int k = n;
        if (n > time) {
            return time + 1;
        }
        n = n - 1;
        time -= n;
        bool i = false;
        while (time > 0) {
            i = !i;
            time -= n;
        }
        if (i) {
            return -(time) + 1;
        }
        return k + time;
    }

    // Logical solution O(1)
    int passThePillow2(int n, int time) {
        int chunks = time / (n - 1);
        return chunks % 2 == 0 ? (time % (n - 1) + 1) : (n - time % (n - 1));
    }
};

// Function to run test cases
void runTestCase(int n, int time, int expected) {
    Solution sol;
    int result = sol.passThePillow(n, time);
    if (result == expected) {
        cout << "Test case passed" << endl;
    } else {
        cout << "Test case failed" << endl;
        cout << "Expected: " << expected << ", but got: " << result << endl;
    }
}

int main() {
    runTestCase(4, 5, 2);
    return 0;
}