from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from kivy.clock import Clock
from seconds import Seconds
from pygame import mixer
from sits import Sits
from runner import Runner
from kivy.properties import NumericProperty
age = 7
name = ""
p1, p2, p3 = 0, 0, 0

def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False


class ScrButton(Button):
    def __init__(self, screen, direction='right', goal='main', **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.direction = direction
        self.goal = goal
    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InstrScr(name='main'))
        sm.add_widget(PulseScr(name='pulse1'))
        sm.add_widget(Otdix(name='sits'))
        sm.add_widget(PulseScr2(name='pulse2'))
        sm.add_widget(Result(name='result'))
        return sm
class InstrScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        instr = Label(text=txt_instruction)
        lbl1 = Label(text='Введите имя:', halign='right')
        self.in_name = TextInput(multiline=False)
        lbl2= Label(text='Введите возраст:', halign='right')
        self.in_age = TextInput(text='', multiline=False)
        self.btn = Button(text='Начать', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
        self.btn.on_press = self.next
        purple = (.138,.43,.222, 1)
        Window.clearcolor = purple
        l1 = BoxLayout(size_hint=(0.8, None), height='30sp')
        l2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        l1.add_widget(lbl1)
        l1.add_widget(self.in_name)
        l2.add_widget(lbl2)
        l2.add_widget(self.in_age)
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(l1)
        outer.add_widget(l2)
        outer.add_widget(self.btn)
        self.add_widget(outer)
    def next(self):
        name = self.in_name.text
        age = check_int(self.in_age.text)
        if age == False or age < 7:
            age = 7
            self.in_age.text = str(age)
        else:
            self.manager.current = 'pulse1'

class PulseScr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        instr = Label(text=txt_test1)
        self.lbl_sec = Seconds(2)
        self.lbl_sec.bind(done=self.sec_finished)
        l1 = BoxLayout(size_hint=(0.4, None), height='30sp')
        
        
        
        lbl1 = Label(text='Введите результат:', halign='right')
        self.in_result = TextInput(text='0',multiline=False)
        self.btn = Button(text='Продолжить', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5})
        self.btn.on_press = self.next
        l1.add_widget(lbl1)
        l1.add_widget(self.in_result)
        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.lbl_sec)
        outer.add_widget(l1)
        self.line3 = BoxLayout(size_hint=(0.5, None), pos_hint={'center_x': 0.5})
        self.line3.add_widget(self.btn)
        outer.add_widget(self.line3)
        self.add_widget(outer)
    
    def sec_finished(self, *args):
        self.next_screen = True
        self.in_result.set_disabled(False)
        self.btn.set_disabled(False)
        self.btn.text = 'Продолжить'

        
        self.line3.remove_widget(self.btn)
        self.line3.add_widget(self.btn)
    def next(self):
        mixer.init()
        mixer.music.stop() 
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.lbl_sec.start()
        else:
            global p1
            p1 = check_int(self.in_result.text)
            if p1 == False or p1 <= 0:
                p1 = 0
                self.in_result.text = str(p1)
            else:
                self.manager.current = 'sits'

class Otdix(Screen):
    sit = NumericProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        total_sits = 30
           
        row1 = BoxLayout(orientation='vertical')
        instr = Label(text=txt_test2, halign = 'center')
        lbl_sits = Sits(total_sits)
        self.run = run = Runner(total=total_sits, steptime=1.5, size_hint=(0.5, 1), pos_hint={'center_x': 0.5})
        run.bind(value=lbl_sits.next)
        run.bind(finished=self.finished)
                
        row1.add_widget(instr)
        row1.add_widget(lbl_sits)
        row1.add_widget(run)

        self.btn = btn = Button(text='Начать', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})

        btn.on_press = self.next

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(row1)
        outer.add_widget(btn)
        self.add_widget(outer)
    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.run.start()
        else:
            self.manager.current = 'pulse2'
    
    def finished(self, *args):
        self.btn.set_disabled(False)
        self.next_screen = True
        self.btn.text = "Дальше"
class PulseScr2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen = False
        self.stage = 0

        instr = Label(text=txt_test3)

        self.lbl1 = Label(text='Считайте пульс')
        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done=self.sec_finished)

        line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
        lbl_result2 = Label(text='Результат:', halign='right')
        self.in_result2 = TextInput(text='0', multiline=False)
        self.in_result2.set_disabled(True)
        line1.add_widget(lbl_result2)
        line1.add_widget(self.in_result2)
        
        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        lbl_result3 = Label(text='Результат после отдыха:', halign='right')
        self.in_result3 = TextInput(text='0', multiline=False)
        self.in_result3.set_disabled(True)
        line2.add_widget(lbl_result3)
        line2.add_widget(self.in_result3)
        
        self.btn = btn = Button(text='Начать', size_hint=(0.3, 0.5), pos_hint={'center_x': 0.5})
        btn.on_press = self.next

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(instr)
        outer.add_widget(self.lbl1)
        outer.add_widget(self.lbl_sec)
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer.add_widget(self.btn)
        self.add_widget(outer)

    def sec_finished(self, *args):
        
        if self.lbl_sec.done:
            if self.stage == 0:
                self.stage = 1
                self.lbl1.text = 'Отдыхайте'
                self.lbl_sec.restart(2)
                self.in_result2.set_disabled(False)
            elif self.stage == 1:
                self.stage = 2
                self.lbl1.text='Считайте пульс'
                self.lbl_sec.restart(2)
            elif self.stage == 2:
                self.in_result3.set_disabled(False)
                self.btn.set_disabled(False)
                self.btn.text = 'Завершить'
                self.next_screen = True

    def next(self):
        mixer.init()
        mixer.music.stop() 
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.lbl_sec.start()
        else:
            global p2, p3
            p2 = check_int(self.in_result2.text)
            p3 = check_int(self.in_result3.text)
            if not p2 or p2<0:
                p2 = 0
                self.in_result2.text = str(p2)
            elif not p3 or p3<0:
                p3 = 0
                self.in_result3.text = str(p3)
            else:
                self.manager.current = 'result'

class Result(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.instr = Label(text = '')
        self.outer.add_widget(self.instr)
        self.add_widget(self.outer)
        self.on_enter = self.before

    def before(self):
        global name
        self.instr.text = name + '\n' + test(p1, p2, p3, age)


class Result(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.instr = Label(text='')
        self.outer.add_widget(self.instr)
        self.add_widget(self.outer)
        self.on_enter = self.before

    def before(self):
        global name
        self.instr.text = name + '\n' + test(p1, p2, p3, age)


        



        

  
app = MyApp()
app.run()