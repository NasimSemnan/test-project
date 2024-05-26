def sum_min_max(arr):
    if not arr or len(arr) <= 1:
        return 0
    ar_min = min(arr)
    ar_max = max(arr)
    return sum(arr) - ar_min - ar_max


print(sum_min_max([1, 2, 5, 16]))
