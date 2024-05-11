class Log:
    active: bool = True

    def __init__(self, active: bool):
        self.active = False

    def is_active(self):
        return self.active
    
    def add_debug(self, code: str, text: str):
        print(code + ": " + text)

