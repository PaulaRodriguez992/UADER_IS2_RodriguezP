import os
#*--------------------------------------------------------------------
#* Ejemplo de pattern Proxy
#* La clase Door verifica una clave que solo puede ser lograda 
#* mediante la "encriptación" de una clave en texto claro
#*--------------------------------------------------------------------
class Door:
    def open_method(self) -> None:
        pass

    def operation(self, keystr) -> None:
        print("la clave recibida (%s)" %(keystr))
        self.verify(keystr)

    def verify(self, keystr) -> None:
        if keystr == "636c6176650000000000000000000000":
           print("acceso aceptado, puede proceder")
        else:
           print("acceso denegado")

class SecuredDoor:
    def __init__(self) -> None:
        self._klass = Door()

    def open_method(self) -> None:
        print(f"Adding security measure to the method of {self._klass}")

    def operation(self,keystr) -> None:
        if keystr == "clave":
           newkey="636c6176650000000000000000000000"
        else:
           newkey=keystr
        print("la clave recibida por el proxy es (%s) la enviada es (%s)" % (keystr,newkey))
        self._klass.operation(newkey)


#*------------------------------------------------------------
#* main
#*------------------------------------------------------------

os.system("clear")
#*--Crea objeto que no se puede acceder directamente
door = Door()
key="clave"
door.operation(key)

#*-- Crea objeto proxy
secured_door = SecuredDoor()
secured_door.open_method()
secured_door.operation(key)
