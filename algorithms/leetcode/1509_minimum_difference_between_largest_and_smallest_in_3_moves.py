from typing import List


class Solution:
    def minDifference(self, nums: List[int]) -> int:
        if len(nums) <= 4:
            return 0
        else:
            nums.sort()
            ans = nums[-1] - nums[0]
            i = 0
            while i < 4:
                ans = min(ans, nums[-4 + i] - nums[i])
                i += 1

            return ans
