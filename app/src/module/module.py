
class Module():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(__class__, cls).__new__('cls')
        return cls._instance

    def Get_Poll_Object():
        pass