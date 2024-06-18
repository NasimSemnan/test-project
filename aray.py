def array_to_csv(arr):
    csv_str = ""
    for row in arr:
        csv_str += ",".join(map(str, row)) + "\n"
    return csv_str.rstrip("\n")


input_arr = [
    [0, 1, 2, 3, 4],
    [10, 11, 12, 13, 14],
    [20, 21, 22, 23, 24],
    [30, 31, 32, 33, 34],
]

csv_output = array_to_csv(input_arr)
print(csv_output)
