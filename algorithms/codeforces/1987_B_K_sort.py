# link : https://codeforces.com/contest/1987/problem/B
from typing import List


def func(n: int, a: List):
    pref_max = s = mx = 0
    for i in range(n):
        pref_max = max(pref_max, a[i])
        d = pref_max - a[i]
        s += d
        mx = max(mx, d)
    return s + mx


def get_input():
    no_of_test_cases = int(input())
    test_cases = []
    for _ in range(no_of_test_cases):
        n = int(input())
        a = list(map(int, input().split()))
        test_cases.append((n, a))
    return no_of_test_cases, test_cases


if __name__ == "__main__":
    _, inp = get_input()
    results = []
    for lst in inp:
        print(func(*lst))
