class Matrix:
    def array_to_csv(arr):
        csv_str = ""
        for row in arr:
            csv_str += ",".join(map(str, row)) + "\n"
        return csv_str.rstrip("\n")

    def w_csv(csv_str, file2):
        with open(file2, "w") as file:
            file.write(csv_str)


output_csv = array_to_csv(input_arr)
w_csv(output_csv, "output.csv")
print(output_csv)
Matrix.array_to_csv()
Matrix.w_csv()
print(Matrix.w_csv)
