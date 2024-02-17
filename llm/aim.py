class BaseLLM:
    def __init__(self) -> None:
        pass

class Cutter(BaseLLM):
    def __init__(self) -> None:
        self.prompt = 'Сократи этот текст: '
        self.completed = False

    def cut(self):
        #Код сокращения контекста
        self.completed = True

class ShortMemory:
    def __init__(self) -> None:
        self.cutter = Cutter()
