import tkinter as tk
from classMatrix import Matrix
from tabulate import tabulate
import gui_functions as gui_func




root = tk.Tk()
root.title('Matrix calculator')
app_width = 1000
app_height = 500
geometry = str(app_width) + 'x' + str(app_height)
root.geometry(geometry)

#Creating matrices
matrix_a, matrix_a_entries = gui_func.matrix_widget(root, 3, 3, 'Matrix A', height = app_height / 3, width = app_width / 3)
matrix_a.place(x = 0, y = 50)

matrix_b,  matrix_b_entries = gui_func.matrix_widget(root, 3, 3, 'Matrix B', height = app_height / 3, width = app_width / 3)
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
    a_entries = gui_func.read_matrix(matrix_a_entries)
    b_entries = gui_func.read_matrix(matrix_b_entries)
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
