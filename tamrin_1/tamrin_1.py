def sum_min_max(lst):
    if not lst:
        return None

    min_value = lst[0]
    max_value = lst[0]
    for num in lst:
        if num < min_value:
            min_value = num
        elif num > max_value:
            max_value = num

    return sum(lst) - min_value - max_value


my_list = [5, 10, 2, 1]
my_list2 = [11, 15, 5, 6, 3]
print(sum_min_max(my_list))
print(sum_min_max(my_list2))
