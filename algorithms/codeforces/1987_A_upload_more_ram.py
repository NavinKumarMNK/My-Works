# link : https://codeforces.com/contest/1987/problem/A
def func(n: int, tw: int):
    return (tw * (n - 1)) + 1


def get_input():
    no_of_test_cases = int(input())
    inputs = []
    for _ in range(no_of_test_cases):
        inputs.append(map(int, input().split()))
    return no_of_test_cases, inputs


if __name__ == "__main__":
    _, inp = get_input()
    results = []
    for lst in inp:
        print(func(*lst))
