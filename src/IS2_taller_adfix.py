import os
#*--------------------------------------------------------------------
#* Ejemplo de pattern adapter
#* La clase Adapter invoca a la clase original agregando un parametro
#*--------------------------------------------------------------------
class Adaptee:
    def open_method(self) -> None:
        pass

    def operation(self, p1, p2) -> None:
        print("\nlos parámetros recibidos son (%s-%s)\n" %(p1,p2))

class Adapter:
    def __init__(self) -> None:
        self._klass = Adaptee()

    def open_method(self) -> None:
        print(f"Adding security measure to the method of {self._klass}")

    def operation(self,p1) -> None:
        self._klass.operation(p1,"fake p2")


#*------------------------------------------------------------
#* main
#*------------------------------------------------------------
os.system("clear")

#*--Crea objeto que no se puede acceder directamente
adaptee = Adaptee()

try:
	key="clave"
	adaptee.operation(key)

except Exception as e:
	print("Excepción llamando adaptee.operation(\"%s\") e(%s)\n" % (key,e))

#*-- Crea objeto adapter
adapter = Adapter()
adapter.open_method()
adapter.operation(key)
