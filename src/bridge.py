#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Bridge
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------

"""
El siguiente código NO usa un patrón bridge

Se dispone de una clase con tres atributos (largo,ancho y alto) y tres
métodos llamados ProduceWithAPI1(), ProduceWithAPI2() y expand().
"""

class Cuboid:

    class ProducingAPI1:

        """Esta es una implementación específica para el Cuboid cuando usa el API1"""

        def produceCuboid(self, length, breadth, height):
            print("El Cuboid es producido por API1 con dimensiones {%d,%d,%d}\n" % (length,breadth,height))

    class ProducingAPI2:
        """Esta es una implementación específica para el Cuboid cuando usa el API2"""

        def produceCuboid(self, length, breadth, height):
            print("El Cuboid es producido por API2 con dimensiones {%d,%d,%d}\n" % (length,breadth,height))


    def __init__(self, length, breadth, height):

        """Inicializar las dimensiones del dispositivo"""

        self._length = length
        self._breadth = breadth
        self._height = height

    def produceWithAPI1(self):

        """Implementation specific Abstraction"""

        objectAPIone = self.ProducingAPI1()
        objectAPIone.produceCuboid(self._length, self._breadth, self._height)

    def producewithAPI2(self):

        """Implementation specific Abstraction"""

        objectAPItwo = self.ProducingAPI2()
        objectAPItwo.produceCuboid(self._length, self._breadth, self._height)

    def expand(self, times):

        """Implementation independent Abstraction"""

        self._length = self._length * times
        self._breadth = self._breadth * times
        self._height = self._height * times


"""
*******************************************************************************************
                             Bridge Adapter
*******************************************************************************************
"""

"""
Ahora implementa el código con el patrón Bridge, a las dimensiones
del objeto a construir se le agrega el API a utilizar como un
parámetro mas, separando la abstracción de la implementación
"""

class ProducingAPI1:

    def produceCuboid(self, length, breadth, height):
        print("*BRIDGE* El Cuboid es producido por API1 con dimensiones {%d,%d,%d}\n" % (length,breadth,height))


class ProducingAPI2:

    """Implementation specific Abstraction"""

    def produceCuboid(self, length, breadth, height):
        print("*BRIDGE* El Cuboid es producido por API2 con dimensiones {%d,%d,%d}\n" % (length,breadth,height))


class CuboidBridge:

    def __init__(self, length, breadth, height, producingAPI):

        """Initialize the necessary attributes
           Implementation independent Abstraction"""

        self._length = length
        self._breadth = breadth
        self._height = height

        self._producingAPI = producingAPI

    def produce(self):

        """Implementation specific Abstraction"""

        self._producingAPI.produceCuboid(self._length, self._breadth, self._height)

    def expand(self, times):

        """Implementation independent Abstraction"""

        self._length = self._length * times
        self._breadth = self._breadth * times
        self._height = self._height * times




"""
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
"""

# Instantiate a Cuboid
import os
os.system('clear')

print("Este es un ejemplo que no utiliza el pattern Bridge")

cuboid1 = Cuboid(1, 2, 3)
cuboid1.produceWithAPI1()


# Instantiate another Cuboid
cuboid2 = Cuboid(19, 20, 21)
cuboid2.producewithAPI2()

print("\nAhora con el uso del patrón BRIDGE\n")

cuboid1 = CuboidBridge(1, 2, 3, ProducingAPI1())
cuboid1.produce()

cuboid2 = CuboidBridge(19, 20, 21, ProducingAPI2())
cuboid2.produce()




