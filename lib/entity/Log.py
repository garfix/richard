class Log:
    active: bool = False

    def is_active(self):
        return self.active
    
    def add_debug(self, code: str, text: str):
        print(code + ": " + text)

