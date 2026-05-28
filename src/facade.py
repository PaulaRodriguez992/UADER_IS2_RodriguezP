#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Facade
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------

""" 
    Se dispone de tres clases separadas e independientes entre si 
    emulando tres sub-sistemas diferentes que deben ser invocados 
    para completar una transacción por parte de un determinado código
    de cliente, estas clases (sub-sistemas) son:

         Inventory
         Payment
         Notification
"""

""" Inventory """

class Inventory:
    def check_stock(self, product_id):
        print("Se verifica el stock para el producto solicitado %s\n" % (product_id))
        return True

    def update_stock(self, product_id, quantity):
        print("Se ajusta el stock del producto (%s) reduciendo la cantidad en %d\n" % (product_id,quantity))

""" Payment """

class Payment:
    def process_payment(self, amount):
        print("Procesando el pago de $%d\n" % (amount))
        return True

""" Notification """

class Notification:
    def send_confirmation(self, order_id):
        print("Enviando confirmación para la orden %s\n" % (order_id))

""" Facade para los sub-sistemas anteriores """

class OrderFacade:
    def __init__(self):
        self.inventory = Inventory()
        self.payment = Payment()
        self.notification = Notification()

    def place_order(self, product_id, quantity, amount):
        if self.inventory.check_stock(product_id):
            if self.payment.process_payment(amount):
                self.inventory.update_stock(product_id, -quantity)
                self.notification.send_confirmation(product_id)
                print("La orden fue procesada correctamente")
            else:
                print("El proceso de la orden ha fallado")
        else:
            print("No hay stock del producto")

if __name__ == "__main__":

    import os
    os.system('clear')

    print("Primero se implementa el cliente mediante la interacción directa\n")

    i=Inventory()
    p=Payment()
    n=Notification()

    """ Los datos de la orden son """
    product_id=1
    quantity=1
    amount=100

    if i.check_stock(product_id):
       if p.process_payment(amount):
          i.update_stock(product_id,-quantity)
          n.send_confirmation(product_id)
          print("La orden fue procesada correctamente llamando a los sub-sistemas\n")
       else:
          print("El pago ha fallado")
    else:
       print("No hay stock para el producto %s\n" % (product_id))

    """ Ahora procesa usando Facade """

    print("\nAhora procesa usando Facade\n")
    facade = OrderFacade()
    facade.place_order(product_id=1, quantity=1, amount=100)

