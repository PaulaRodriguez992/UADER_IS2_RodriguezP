#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Flyweight
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------

class ComplexCars(object):

    """Clase separada para definir autos complejos"""

    def __init__(self):
        pass

    def cars(self, car_name):
        return "Auto de patrón complejo [% s]\n" % (car_name)


class CarFamilies(object):

    """Almacena los ID de autos complejos en un diccionario"""

    car_family = {}
    def __new__(cls, name, car_family_id):
        try:
            id = cls.car_family[car_family_id]
        except KeyError:
            id = object.__new__(cls)
            cls.car_family[car_family_id] = id
        return id

    def set_car_info(self, car_info):
        cg = ComplexCars()
        self.car_info = cg.cars(car_info)

    def get_car_info(self):
        return (self.car_info)



if __name__ == '__main__':

    import os
    os.system('clear')


    """ Genera diccionario con distintos tipos de auto y sus caracteristicas """

    car_data = (('a', 1, 'Audi'), ('a', 2, 'Ferrari'), ('b', 1, 'Audi'))

    car_family_objects = []
    for i in car_data:
        obj = CarFamilies(i[0], i[1])
        obj.set_car_info(i[2])
        car_family_objects.append(obj)

    """Iguales ID implica los mismos objetos """

    for i in car_family_objects:
        print("id = " + str(id(i)))
        print(i.get_car_info())

