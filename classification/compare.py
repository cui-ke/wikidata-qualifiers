import csv

def compare_csv_files(file1_path, file2_path):
    with open(file1_path, mode='r', newline='') as file1, open(file2_path, mode='r', newline='') as file2:
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)

        for row_index, (row1, row2) in enumerate(zip(reader1, reader2)):
            for col_index in range(min(20, len(row1), len(row2))):
                if row1[col_index+1] != row2[col_index]:
                    print(f"Difference found at row {row_index + 1}, column {col_index + 1}:")
                    print(f"File 1: '{row1[col_index+1]}'")
                    print(f"File 2: '{row2[col_index]}'")

# Example usage
file1_path = 'Qualifier_2025-01-01_Analysis_b.csv'
file2_path = 'Qualifier_2025-01-01_Analysis.csv'
compare_csv_files(file1_path, file2_path)
