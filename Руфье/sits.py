# напиши модуль для подсчета количества приседаний
from kivy.uix.label import Label
class Sits(Label):   
    def __init__(self, total, **kwargs):
        self.current = 0
        self.total = total
        text21 = 'Осталось приседаний:' + str(30)
        super().__init__(text=text21, **kwargs)
    def next(self, *args):
        self.current += 1
        remain = max(0,self.total - self.current)
        self.text = 'Осталось приседаний:' + str(remain)
