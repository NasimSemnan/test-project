import csv
import random

from arry_csv import Matrix


class MatrixGenerator:
    def __init__(self):
        self.items: list[Matrix] = []

    def add_matrix(self):
        max_row = int(input("satr matrix: "))
        max_col = int(input("soton matrix: "))

        # matrix = [[]]
        # for _ in range(max_row):
        #     row_values = []
        #     for _ in range(max_col):
        #         row_values.append(random.uniform(0, 1))

        #     matrix.append(row_values)

        matrix = [
            [random.uniform(0, 1) for i in range(max_row)]
            for j in range(max_col)
        ]

        instance = Matrix(matrix)
        self.items.append(instance)

    def add_matrix_from_csv(self, path: str):
        with open(path, "r") as file:
            reader = csv.reader(file)

            # 1st method
            # data = []
            # for reader_row in reader:
            #     row = []
            #     for reader_col in reader_row:
            #         row.append(float(reader_col))

            #     data.append(row)

            # 2nd method
            data = [(float(col) for col in row) for row in reader]

            instance = Matrix(data)
            self.items.append(instance)

        # remove the matrix index

    def remove(self, index: int):
        del self.items[index]
        print(f"andis {index} pak shod")

    def print_csv(self):
        for matrix in self.items:
            matrix.print()
            print("\n")

    def clean(self):
        self.items = []


# generator = MatrixGenerator()

# generator.add_matrix()
# generator.add_matrix()

# generator.print_csv()

generator = MatrixGenerator()
while True:
    nam = input("Harf vard kon a, af, p, q, c, r:\n")

    if nam == "a":
        generator.add_matrix()
    elif nam == "p":
        generator.print_csv()
    elif nam == "q":
        break
    elif nam == "af":
        path = input("Enter the csv file path:\n")
        generator.add_matrix_from_csv(path)
        # kamel konid :)
    elif nam == "r":
        index = int(input("index vared kon: \n"))
        generator.remove(index)
        print("ekiaz matrix ha hazzf shod")

    elif nam == "c":
        generator.clean()
        print("list matrix hazf shod")
