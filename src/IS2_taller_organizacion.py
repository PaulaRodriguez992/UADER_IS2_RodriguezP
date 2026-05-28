import os
#*--------------------------------------------------------------------
#* Ejemplo de pattern composite
#* Se genera una clase LeafElement que representa nodos terminales y una
#* CompositeLement que representa al arbol (de CompositeElement y LeafElement)
#* que de el dependen.
#*--------------------------------------------------------------------

#*------------- Define una clase para los nodos terminales (leaf)
class LeafElement:

	def __init__(self, *args):

#*--- indenta las posiciones a medida que se agregan
		self.position = args[0]

#*--- lista elementos

	def showDetails(self):

		'''Prints the position of the child element.'''
		print("\t", end ="")
		print(self.position)

#*---- Elemento compuesto, representa objetos en cualquier nivel de la jerarquia excepto el último

class CompositeElement:

	def __init__(self, *args):

		self.position = args[0]
		self.children = []

#*----- Crea jerarquia

	def add(self, child):

		self.children.append(child)

#*---- Remueve jerarquia

	def remove(self, child):

		self.children.remove(child)

#*---- muestra detalles (itera a los niveles inferiores


	def showDetails(self):

		print(self.position)
		for child in self.children:
			print("\t", end ="")
			child.showDetails()


"""main method"""

if __name__ == "__main__":

	os.system("clear")

#*------ Crea el top level de la jerarquia

	topLevelMenu = CompositeElement("CIO")

#*----- Crea la primer gerencia

	subMenuItem1 = CompositeElement("Gerencia desarrollo (Java)")

	subMenuItem11 = LeafElement("Desarrollador Java #1")
	subMenuItem12 = LeafElement("Desarrollador Java #2")

	subMenuItem1.add(subMenuItem11)
	subMenuItem1.add(subMenuItem12)

#*---- Crea la segunda gerencia

	subMenuItem2 = CompositeElement("Gerencia de Test")

	subMenuItem21 = LeafElement("Tester #1")
	subMenuItem22 = LeafElement("Tester #2")

	subMenuItem2.add(subMenuItem21)
	subMenuItem2.add(subMenuItem22)

#*---- Agrega ahora las dos gerencias al nivel raiz

	topLevelMenu.add(subMenuItem1)
	topLevelMenu.add(subMenuItem2)

#*---- Muestra el resultado
	topLevelMenu.showDetails()


#*---- Agrega una nueva gerencia de desarrollo

	print("\n agrega una nueva gerencia Python\n")
	subMenuItem3 = CompositeElement("Gerencia de Desarrollo (Python)")

	subMenuItem31 = LeafElement("Desarrollador Python #1")
	subMenuItem32 = LeafElement("Desarrollador Python #2")
	subMenuItem33 = LeafElement("Desarrollador Python #3")

	subMenuItem3.add(subMenuItem31)
	subMenuItem3.add(subMenuItem32)
	subMenuItem3.add(subMenuItem33)

	topLevelMenu.add(subMenuItem3)

#*---- Muestra el resultado
	topLevelMenu.showDetails()

#*---- Muestra el resultado

	topLevelMenu.showDetails()

	print("Remueve a la gerencia #3 recién agregada\n")
	topLevelMenu.remove(subMenuItem3)
	topLevelMenu.showDetails()

