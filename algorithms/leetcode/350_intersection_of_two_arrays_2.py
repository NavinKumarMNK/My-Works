from typing import List


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        if len(nums1) < len(nums2):
            nums2, nums1 = nums1, nums2

        nums1.sort()
        nums2.sort()

        i = j = 0
        result = []
        while i < len(nums1) and j < len(nums2):
            if nums1[i] == nums2[j]:
                result.append(nums1[i])
                i += 1
                j += 1
            elif nums1[i] > nums2[j]:
                j += 1
            elif nums1[i] < nums2[j]:
                i += 1

        return result


if __name__ == "__main__":
    # Default test case inputs
    nums1 = [1, 2, 2, 1]
    nums2 = [2, 2]

    obj = Solution()
    result = obj.intersect(nums1, nums2)
    assert result == [2, 2]
