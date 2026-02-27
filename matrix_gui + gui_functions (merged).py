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
            print(grid_entry)
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


root = tk.Tk()
root.title('Matrix calculator')
app_width = 1000
app_height = 500
geometry = str(app_width) + 'x' + str(app_height)
root.geometry(geometry)

#Creating matrices
matrix_a, matrix_a_entries = matrix_widget(root, 3, 3, 'Matrix A', height = app_height / 3, width = app_width / 3)
matrix_a.place(x = 0, y = 50)

matrix_b,  matrix_b_entries = matrix_widget(root, 3, 3, 'Matrix B', height = app_height / 3, width = app_width / 3)
matrix_b.place(x = app_width * 0.5, y = 50)

#Operator selection
operators  = ('+', '-', '*')
operator = tk.StringVar()
operator_y = 57
for sign in operators:
    operator_choice = tk.Radiobutton(root, text = sign, value = sign, variable = operator )
    operator_choice.place(x = app_width *0.35, y = operator_y)
    operator_y += 30

#Creating result display 
result_matrix = tk.StringVar()
result = tk.Label(root, textvariable = result_matrix)
result.place(x = app_width * 0.8, y = 70)

#Calculation function
def calculate():
    a_entries = read_matrix(matrix_a_entries)
    b_entries = read_matrix(matrix_b_entries)
    a = Matrix(*a_entries)
    b = Matrix(*b_entries)
    if operator.get() == '+':
        result = a + b
    elif operator.get() == '-':
        result = a - b    
    elif operator.get() == '*':
        result = a * b
    else:
        result_matrix.set('Select an operator.')
        return None
    print_result = tabulate(result.entries)
    result_matrix.set(print_result)
#Calculation button    
calc = tk.Button(root, text ='Calculate', command = calculate)
calc.place(x = app_width * 0.8, y = 40)

    
root.mainloop()
