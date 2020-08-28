class ProblematicNames:
    def __init__(self, name, category):
        self.__name = name
        self.__category = category

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, var):
        self.__name = var

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, var):
        self.__category = var
