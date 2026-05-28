#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Iterator (native Python implementation)
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

import os
os.system('clear')

my_list = [4, 5, 6]
my_iter = MyIterator(my_list)

for item in my_iter:
    print(item)
