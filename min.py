def find_max_min(list):
    max = 0
    min = list[0]
    for i in list:
        if i > max:
            max = i
        if i < min:
            min = 1
    return (min, max)


m = [1, 2, 5, 50]
min, max = find_max_min(m)
print(min, max)


def sum_list(list, min, max):
    sum = 0
    for i in list:
        if i != min and i != max:
            sum = sum + i
    return sum


print(sum_list(m, min, max))
