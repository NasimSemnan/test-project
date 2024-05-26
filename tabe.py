def find_greater_than(num, astane):
    result = []
    for n in num:
        if num > astane:
            result.append(num)
    return result


print(find_greater_than([-3, 2, 8, 15, 31, 5, 4, 8], 5))
