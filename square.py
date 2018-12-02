class superior():
    number = 0
    number_alive = 0

class square(superior):

    number = 0
    
    def __init__(self, row, column, x, y, number_of_columns, size):
        self.row = row
        self.column = column
        self.x = x
        self.y = y
        self.number_of_columns = number_of_columns
        self.size = size
        self.live = False
        
        superior.number += 1

    @property
    def is_first_row(self):
        return (self.row == 0)
    
    @property
    def is_last_row(self):
        return (self.row == self.number_of_columns - 1)
    
    @property
    def is_first_column(self):
        return (self.column == 0)
    
    @property
    def is_last_column(self):
        return (self.column == self.number_of_columns - 1)

    def is_in_range(self, x, y):
        if x in range(self.x, self.x + self.size + 1) and y in range(self.y, self.y + self.size + 1):
            return True
        else:
            return False
    
    @property
    def alive(self):
        return self.live
    
    @alive.setter
    def alive(self, isalive):
        if self.live and not isalive:
            superior.number_alive -= 1
        elif not self.live and isalive:
            superior.number_alive += 1

        self.live = isalive

        
            
        

