from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from sudoku_solver import solveSudoku,isValidSudoku
from random import randint
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

class ColorLabel(Label):
    def __init__(self, square,**kwargs):
        super(ColorLabel, self).__init__(**kwargs)
        self.square = square
        with self.canvas.before:
            # Set the background color here
            Color(1, 1, 1, 1)  # RGBA values (white)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class NumTextInput(TextInput):
    def insert_text(self,substring,from_undo=False):
        nums = '1234567890'
        if len(self.text)>=1:
            s = ''
        elif substring in nums:
            s = substring
        return super().insert_text(s, from_undo=from_undo)

#page 1
class Sudoku(BoxLayout):
    def __init__(self,**kwargs):
        super(Sudoku, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.sudoku_image = Image(source='sudoku_image.jpg',size_hint = (1,.3),pos_hint = {'top':1})
        self.add_widget(self.sudoku_image)
        self.start_game = Button(text = "Generate game",font_size = 30,size_hint = (1,.3), pos_hint = {'center_y':1})
        self.start_game.bind(on_press = self.switch)
        self.add_widget(self.start_game)
    
    def switch(self,item):
        App.get_running_app().screen_manager.current = 'Second'

#page 2
class Game(GridLayout):
    def __init__(self,**kwargs):
        super(Game, self).__init__(**kwargs)
        self.rows = 10
        self.cols = 10
        self.game_started = False
        self.game_bd = None
        self.btn = Button(text = "Start")
        self.btn.bind(on_press = self.start_game)
        self.add_widget(self.btn)

    def start_game(self,*args):
        bd = [['.' for i in range(9)] for i in range(9)]
        nums = [str(i) for i in range(1,10)]
        nums2 = nums[:]
        for c,i in enumerate(bd):
            r = randint(0,len(nums)-1)
            rand_num = randint(0,len(nums2)-1)
            while nums2[rand_num] == nums[r]:
                rand_num = randint(0,len(nums2)-1)
            bd[c][randint(3,8)] = nums.pop(r)
            bd[c][0] = nums2.pop(rand_num)
        bd = solveSudoku(bd)
        self.game_bd = bd[:]
        for c in range(len(self.game_bd)):
            for n in range(4):
                self.game_bd[c][randint(0,8)] = '.'
        self.remove_widget(self.btn)
        self.game_running()
    
    def reset(self):
        self.game = self.game_bd
        
    def game_running(self):
        self.empties = 0
        tb = []
        for c,i in enumerate(self.game_bd):
            sq = ''
            if (c + 1)%3 == 0:
                if c != 8:
                    sq += 'v'
            for n,j in enumerate(i):
                if j == '.':
                    #add sq back in later
                    self.empties += 1
                    box = NumTextInput(background_color = [1,1,1,1],font_size = 20, multiline=False, size_hint = (1,1), padding=10)
                    tb.append(box)
                else:
                    box = ColorLabel(sq,text = j, color = [0,0,0,1],padding=10)
                self.add_widget(box)
            if c == 0:
                self.game_reset = Button(text="Reset board")
                self.game_reset.bind(on_press=self.reset)
                self.add_widget(self.game_reset)
            else:
                self.lbl = Label()
                self.add_widget(self.lbl)
        self.game = self.game_bd[:]
        self.filled = 0

class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.firstpage = Sudoku()
        screen = Screen(name='First')
        screen.add_widget(self.firstpage)
        self.screen_manager.add_widget(screen)

        self.secondpage = Game()
        screen = Screen(name='Second')
        screen.add_widget(self.secondpage)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager

if __name__ == "__main__":
    MyApp().run()