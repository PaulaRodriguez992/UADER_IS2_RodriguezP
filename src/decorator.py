#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Decorator
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------

class WrittenText:

    def __init__(self, text):
        self._text = text

    def render(self):
        return self._text

class UnderlineWrapper(WrittenText):

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return "<underline>%s</underline>" % (self._wrapped.render())

class ItalicWrapper(WrittenText):


    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return "<italics>%s</italics>" % (self._wrapped.render())

class BoldWrapper(WrittenText):

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self):
        return "<bold>%s</bold>" % (self._wrapped.render())


if __name__ == '__main__':

    import os
    os.system('clear')

    before_gfg = WrittenText("UADER decorator pattern")
    after_gfg = ItalicWrapper(UnderlineWrapper(BoldWrapper(before_gfg)))

    print("Antes de decorator el texto era: \"%s\"\n" % (before_gfg.render()))
    print("Despues de decorator el texto queda \"%s\"\n" % (after_gfg.render()))


