import math
import random
from tabulate import tabulate

class Matrix:
    def __init__(self, *entries, check_entries = False):
        if not isinstance(entries, (list, tuple, set)):
            raise TypeError('Entries are neither list, tuple nor set')
        elif not check_entries:
            self.m = len(entries)
            self.n = len(entries[0])
            entries = tuple([tuple(row) for row in entries])
            self.entries = entries          
        else:
            previous_n_columns=None
            matrix=[] 
            longest_entries=[0]* len(entries[0])   #I'll probably use it later to encode nice displaying for matrices
            for row in entries:
                n_columns = len(row)
                if previous_n_columns != n_columns and previous_n_columns != None:
                    raise TypeError('Cannot create a matrix: Different lengths of rows')
                cleaned_row=[]
                for i, entry in enumerate(row):
                    try:
                        cleaned_row.append(float(entry))
                    except (ValueError, TypeError):
                        raise TypeError('Non-numeric entry')
                    #Finding longest entry in ith column, useful for nice matrix representation
                    entry_length=len(str(float(entry)))
                    if longest_entries[i] < entry_length:
                        longest_entries[i] = entry_length
                previous_n_columns = n_columns
                
                cleaned_row = tuple(cleaned_row)
                matrix.append(cleaned_row)
            self.m = len(matrix)
            self.n = n_columns
            self.entries = tuple(matrix)
            self.longest_entries = longest_entries
        
    def row(self, i):
        row=self.entries[i]
        return list(row)
    def column(self, i):
        return [self.entries[j][i] for j in range(self.n)]
                
    #def __str__(self):
        #longest_in_column  = lambda i : max([len(str(self.entries[j][i])) for j in range(self.n)])
        #row = lambda a : '/n'.join( str(entry).ljust(longest_in_column(i)) for i, entry in enumerate(self.row(a)))
        #return(f'{self.m}*{self.n} Matrix:\n{[row(n_row) for n_row in range(self.m)]}')
    def __str__(self):
        return f'{tabulate(self.entries)}'
    

    def size(self):
        return (self.m, self.n)
    def __add__(self, other):
        if not self.size() == other.size():
            raise TypeError(f'Matrices must be the same size for addition./n You tried to add {self.size()} and {other.size()} matrices.')
        result=[]
        for row1, row2 in zip(self.entries, other.entries):
            row=[]
            for entry1, entry2 in zip(row1, row2):
                row.append(entry1 + entry2)
            result.append(row)
        return Matrix(*result)

    def __mul__(self, other):
        result=[]
        if isinstance(self, (int, float)):
            return NotImplemented
        
        if isinstance(other, (int, float)):
            for row in self.entries:
                product_row=[]
                for entry in row:
                    new_entry = entry * other
                    product_row.append(new_entry)
                result.append(product_row)
                
        elif not self.n == other.m:
            raise TypeError(f'Wrong matrix size for mutiplication./n You tried to multiply {self.size()} and {other.size()} matrices.')
        
        else:
            for i in range(self.m):
                product_row=[]
                for j in range(other.n):
                    column_other = (other.entries[k][j] for k in range(self.n))
                    entry = sum(ent1 * ent2 for ent1, ent2 in zip(self.entries[i], column_other))
                    product_row.append(entry)
                result.append(product_row)
        return Matrix(*result)
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __sub__(self, other):
        return self + other * (-1)
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return self * ( -1)
    
    def __pow__(self, scalar):
        if not isinstance(scalar, int):
            raise TypeError('Tried to take non-integer power of a matrix')
        if not self.m == self.n:
            raise TypeError('Cannot take a power of a non-square matrix')
        
        if scalar > 0:
            result = self
            for i in range(scalar - 1):
                result = result * self
        elif scalar < 0:
            inverse = self.inverse()
            result = inverse
            for i in range( - 1 - scalar):
                result = result * inverse
        else:
            result = Matrix.identity(self.m)
        return result

    def __truediv__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError('Divisor is not a number')
        result=[]
        for row in self.entries:
            new_row=[]
            for entry in row:
                entry = entry/scalar
                new_row.append(entry)
            result.append(new_row)
        return Matrix(*result)
    
    

    def is_square(self):
        return self.m == self.n
    def is_diagonal(self):
        if self.m != self.n:
            return False
        for i in range(self.m):
            for j in range(self.n):
                if i != j and self.entries[i][j] != 0:
                    return False
        return True
    
    def is_upper_triang(self):
        if self.m != self.n:
            return False
        for i in range(self.m):
            for j in range(i):
                if self.entries[i][j] != 0:
                    return False
        return True
    def is_lower_triang(self):
        if self.m != self.n:
            return False
        for i in range(self.m):
            for j in range(i + 1, self.n):
                if self.entries[i][j] != 0:
                    return False
        return True
    
    #def remove_row(self, i):
      
      
    @staticmethod  
    def identity(self, n):
        mtx =[]
        for i in range(n):
            row = []
            for j in range (n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            mtx.append(row)
        return Matrix(*mtx)
        

    def det(self):
        return self.det_from_entries(self.entries)
    

    @staticmethod
    def det_from_entries(entries):
        if not len(entries) == len(entries[0]):
            raise TypeError('Tried to take a determinant of a non-square matrix')
        result=0
        if len(entries) == 2:
            return entries[0][0] * entries[1][1] - entries[1][0] * entries[0][1]
        elif len(entries) == 1:
            return entries[0]
        else:
            for i, entry in enumerate(entries[0]):
                minor = entries[1:]
                minor = [line[:i] + line[(i + 1):] for line in minor]
                minor = tuple(minor)
                cofactor = (-1)**(i) * Matrix.det_from_entries(minor)
                result += cofactor * entry
            return result 
        

    def entries_of_minor(self, entry_row : int, entry_column : int) -> tuple[tuple]:
        if (entry_row > self.m - 1) or (entry_column > self.n - 1):
            raise IndexError("Too big indexes for this matrix. Minor doesn't exist")
        minor : tuple[tuple] = self.entries[:entry_row] + self.entries[(entry_row + 1):]
        minor = [line[:entry_column] + line[(entry_column + 1):] for line in minor]
        return minor


    def cofactor(self,  entry_row : int, entry_column : int) -> int | float:
        submatrix = self.entries_of_minor(entry_row, entry_column)
        sign = (-1) ** (entry_column + entry_row)
        result = Matrix.det_from_entries(submatrix) * sign
        return result


    def transpose(self):
        mx = [ [ self.entries[i][j] for i in range(self.m)] for j in range(self.n)]
        return Matrix(*mx)
    

    def cofactor_matrix(self):
        cofactors = [ [ self.cofactor(j, i) for i in range(self.n)] for j in range(self.m)]  
        return Matrix(*cofactors)
    

    def inverse(self):
        determinant = self.det()
        if determinant == 0:
            raise ZeroDivisionError('Non-invertible matrix - zero determinant')
        cofactors = self.cofactor_matrix()
        result = cofactors.transpose() / determinant
        return result
    
    #@staticmethod
    #def row_mul_number()
    def rref(self):
        mx = [list(row) for row in self.entries]
        print(mx)
        for column in range(self.n):
            for row in range(column, self.m):
                leading_char = mx[row][column]
                if mx[row][column] != 1:
                    normalised_row = []
                    for entry in mx[row]:
                        normalised_row.append(entry / leading_char)
                    mx[row] = normalised_row


        

        return Matrix(*mx)

                                
class Vector:
    def __init__(self, *components, check_entries = False, is_mutable = False):
        self.is_mutable = is_mutable
        if check_entries:
            cleaned=[]
            for component in components:
                try:
                    cleaned.append(float(component))
                except (ValueError, TypeError):
                    raise TypeError('Non-numeric coordinate')
                
        if is_mutable is True:
            self.coordinates = tuple(components)
        elif is_mutable is False:
            self.coordinates = list(components)
        
    def __str__(self):
        return f'Vector{self.coordinates}'
    
    def dimension(self):
        return len(self.coordinates)
    def __len__(self):
        return len(self.coordinates)
    
    
    def __abs__(self):
        return math.sqrt(sum(x**2 for x in self.coordinates))
    def magnitude(self):
        return math.sqrt(sum(x**2 for x in self.coordinates))
    
    def __add__(self, other):
        coordinates=[]
        coordinates1 = self.coordinates
        coordinates2 = other.coordinates
        if len(coordinates1) != len(coordinates2):
            raise TypeError('Different dimesions.')
        for coord1, coord2 in zip(coordinates1, coordinates2):
            coord = coord1 + coord2
            coordinates.append(coord)
        return Vector(*coordinates)
    

    #def __eq__    


    def __sub__(self, other):
        coordinates=[]
        coordinates1 = self.coordinates
        coordinates2 = other.coordinates
        if len(coordinates1) != len(coordinates2):
            raise TypeError('Different dimesions.')
        for coord1, coord2 in zip(coordinates1, coordinates2):
            coord = coord1 - coord2
            coordinates.append(coord)
        return Vector(*coordinates)
    

    def __neg__(self):
        return self*(-1)
    

    #DOT product  or multiply by a scalar  
    def __mul__(self, other):
        if isinstance(self, (int, float)):
            return NotImplemented
        if isinstance(other, (int, float)):
            coordinates = [(coordinate * other) for coordinate in self.coordinates]
            return Vector(*coordinates)
        product=0
        coordinates1 = self.coordinates
        coordinates2 = other.coordinates
        if len(coordinates1) != len(coordinates2):
            raise TypeError('Different dimesions.')
        for coord1, coord2 in zip(coordinates1, coordinates2):
            product += coord1 * coord2
        return product
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError('Divisor is not a number')
        coordinates=[coordinate/scalar for coordinate in self.coordinates]
        return Vector(*coordinates)
    
    @staticmethod
    def angle(v1, v2):
        if (not isinstance(v1, Vector)) or (not isinstance(v2, Vector)):
            raise TypeError('At least 1 argument is not a vector.')
        cos_a = (v1*v2)/(abs(v1)*abs(v2))
        return math.acos(cos_a) * 180 / math.pi
    
    def unit_vect(self):
        magnitude = abs(self)
        if magnitude == 0:
            raise ZeroDivisionError("There's no unit vector for zero vector")
        coordinates=[coordinate/magnitude for coordinate in self.coordinates]
        return Vector(*coordinates)
    
    @classmethod
    def zero(cls, dimension):
        return cls(*[0] * dimension)
  

    def basis_decompose(vector, *basis):
        if len(vector) != len(basis):
            return None
        new_vector 


        
