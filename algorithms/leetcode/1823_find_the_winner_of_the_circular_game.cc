class Solution {
public:
    // Josephus problem is 0-indexed in calculation
    int findTheWinner(int n, int k) {
        int winner = 0;  
        for (int i = 1; i <= n; ++i) {
            winner = (winner + k) % i;
        }
        return winner + 1;  
    }
};