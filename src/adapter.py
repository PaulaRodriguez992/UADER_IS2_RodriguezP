#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* adapter
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
class MotorCycle:

    def __init__(self):
        self.name = "MotorCycle"

    def DosRuedas(self):
        return "<tipo>dos ruedas</tipo>"


class Truck:

    def __init__(self):
        self.name = "Truck"

    def OchoRuedas(self):
        return "<tipo>ocho ruedas</tipo>"


class Auto:

    def __init__(self):
        self.name = "Auto"

    def CuatroRuedas(self):
        return "<tipo>dos ruedas</tipo>"


class Adapter:

    """
   Adapta objetos distintos reemplazando métodos.
   Uso:
    m = Truck()
    m = Adapter(m, wheels = m.DosRuedas)
    """
    import xml.etree.ElementTree as ET 

    def __init__(self, obj, **adapted_methods):
        """Se guarda el objeto en un diccionario"""
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        """Todos los llamados son pasados al objeto para que los resuelva"""
        xml=getattr(self.obj,attr)
        return xml

    def adaptdata(self):
        data=self.wheels()
        data=data.replace('<tipo>','')
        data=data.replace('</tipo>','')
        data="data:\"%s\"" % (data)
        return data

    def original_dict(self):
        """Lista el diccionario del objeto"""
        return self.obj.__dict__


# main method
if __name__ == "__main__":
    import os
    os.system('clear')


    """
    Los distintos métodos involucrados requieren ser llamados a sus métodos
    específicos y devuelven sus respuestas en el formato que originalmente
    utilizaban
    """

    print("Respuestas originales de los objetos individuales")

    o1=MotorCycle()
    print("XML: %s\n%s\n" % (o1.name,o1.DosRuedas()))
    o2=Truck()
    print("XML: %s\n%s\n" % (o2.name,o2.OchoRuedas()))
    o3=Auto()
    print("XML: %s\n%s\n" % (o3.name,o3.CuatroRuedas()))
    print(" ")

    """Lista para almacenar objetos"""
    objects = []

    m = MotorCycle()
    objects.append(Adapter(m, wheels=m.DosRuedas))

    c = Truck()
    objects.append(Adapter(c, wheels=c.OchoRuedas))

    a = Auto()
    objects.append(Adapter(a, wheels=a.CuatroRuedas))

    for obj in objects:
        print("JSON:\n{\"name\":%s,\n\"data\":%s}\n" % (obj.name,obj.adaptdata()))
