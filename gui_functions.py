import tkinter as tk
from classMatrix import Matrix
from tabulate import tabulate

def matrix_widget(parent, rows, columns, label_text, height, width):
    def save_in_file(alias):
        matrix = read_matrix(matrix_entries)
        tabulated = tabulate(matrix)
        with open("database.txt", "a") as database:
            database.write(f'{alias}\n')
            database.write(f'{tabulated}\n')
            database.write('-'*100 + '\n')
    def display_det():
        matrix = read_matrix(matrix_entries)
        det = Matrix.det_from_entries(matrix)
        det_value.set(str(det))
        
    
    matrix = tk.Frame(parent, height = height, width = width)

    label = tk.Label(matrix, text = label_text + ':')
    label.grid(row = 0, column = 0)
    
    name = tk.Entry(matrix, width = 10)
    name.grid(row = 0, column = 1)
    
    matrix_entries = []
    for m in range(1, rows + 1):
        matrix_row =[]
        for n in range(1, columns + 1):
            grid_entry = tk.StringVar()
            entry = tk.Entry(matrix, width = 10, textvariable = grid_entry)
            entry.grid(row = m, column = n)   
            matrix_row.append(grid_entry)
        matrix_entries.append(matrix_row)

    
    save = tk.Button(matrix,
                     text ='Save into file',
                     command = lambda: save_in_file( name.get()))
    save.grid( row = 0, column = 2)
    
    determinant = tk.Button(matrix, text = 'Determinant', command = display_det)
    determinant.grid(row = n+1, column =0)
    
    det_value = tk.DoubleVar()
    display_determinant = tk.Label(matrix, textvariable = det_value)
    display_determinant.grid(row = n+2, column = 0)
    
    return (matrix, matrix_entries)

def read_value(value):
    try:
        entry_for_list = int(value)
    except (ValueError, TypeError):
        entry_for_list = 0
    return entry_for_list
def read_matrix(matrix_entries):  
    mx = [ [read_value(grid_entry.get()) for grid_entry in row] for row in matrix_entries]
    return mx

