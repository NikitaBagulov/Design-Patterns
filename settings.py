class settings:
    __organization_name = ""
    __inn = ""
    __account = ""
    __corr_account = ""
    __bik = ""
    __ownership_type = ""

    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str) or len(value) != 12 or not value.isdigit():
            raise ValueError("ИНН должен содержать 12 цифр!")
        self.__inn = value

    @property
    def account(self):
        return self.__account
    
    @account.setter
    def account(self, value: str):
        if not isinstance(value, str) or len(value) != 11 or not value.isdigit():
            raise ValueError("Счет должен содержать 11 цифр!")
        self.__account = value

    @property
    def corr_account(self):
        return self.__corr_account
    
    @corr_account.setter
    def corr_account(self, value: str):
        if not isinstance(value, str) or len(value) != 11 or not value.isdigit():
            raise ValueError("Корреспондентский счет должен содержать 11 цифр!")
        self.__corr_account = value

    @property
    def bik(self):
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str) or len(value) != 9 or not value.isdigit():
            raise ValueError("БИК должен содержать 9 цифр!")
        self.__bik = value

    @property
    def ownership_type(self):
        return self.__ownership_type
    
    @ownership_type.setter
    def ownership_type(self, value: str):
        if not isinstance(value, str) or len(value) != 5:
            raise ValueError("Вид собственности должен содержать 5 символов!")
        self.__ownership_type = value
