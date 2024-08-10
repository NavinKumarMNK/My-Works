from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# My solution
class Solution:
    def mergeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        count = 0
        temp = head.next
        temp2 = head
        while True:
            if temp.val != 0:
                count += temp.val
            else:
                k = ListNode(count)
                temp2.next = k
                k.next = temp
                count = 0
                temp2 = temp

            temp = temp.next

            if temp is None:
                break

        temp = head.next
        while True:
            if temp is None:
                break
            k = temp.next
            temp.next = k.next
            temp = temp.next
        return head.next


# optimal solution
class Solution:
    def mergeNodes(self, head: ListNode) -> ListNode:
        dummy = ListNode(0)
        current = dummy
        temp = head.next

        count = 0

        while temp:
            if temp.val != 0:
                count += temp.val
            else:
                if count != 0:
                    current.next = ListNode(count)
                    current = current.next
                    count = 0
            temp = temp.next

        return dummy.next


def list_to_linked_list(lst):
    dummy = ListNode()
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linked_list_to_list(head):
    lst = []
    while head:
        lst.append(head.val)
        head = head.next
    return lst


if __name__ == "__main__":
    input_list = [0, 3, 1, 0, 4, 5, 2, 0]
    expected_output = [4, 11]

    input_linked_list = list_to_linked_list(input_list)
    sol = Solution()
    output_linked_list = sol.mergeNodes(input_linked_list)
    output_list = linked_list_to_list(output_linked_list)

    assert (
        output_list == expected_output
    ), f"Expected {expected_output}, but got {output_list}"

    print("Test case passed!")
