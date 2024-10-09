class filter:
    __name: str = ""
    __id: str = ""

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value:str):
        self.__name = value


    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, value:str):
        self.__id = value   