class Matrix:
    def __init__(self, arr):
        self.arr = arr

    def array_to_csv(self):
        csv_str = ""
        for row in self.arr:
            # csv_str += ",".join(f"{num:.2f}" (map(str, row))for num in row) + "\n"
            csv_str += ",".join(f"{num:.2f}" for num in row) + "\n"
        return csv_str.rstrip("\n")

    def w_csv(self, file2):
        csv_str = self.array_to_csv()
        with open(file2, "w") as file:
            file.write(csv_str)

    def print(self):
        print(self.array_to_csv())

    def __str__(self):
        self.array_to_csv()
        return


# matrix = Matrix(
#     [
#         [0, 1, 2, 3, 4],
#         [10, 11, 12, 13, 14],
#         [20, 21, 22, 23, 24],
#         [30, 31, 32, 33, 34],
#     ]
# )
# print(matrix.array_to_csv())

# matrix.w_csv("output.csv")
# matrix.array_to_csv()
