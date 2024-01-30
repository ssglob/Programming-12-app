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
from kivy.clock import Clock

class ColorLabel(Label):
    def __init__(self, **kwargs):
        super(ColorLabel, self).__init__(**kwargs)
        with self.canvas.before:
            # Set the background color here
            Color(1, 1, 1, 1)  # RGBA values (white)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class SquareLabel(Label):
    def __init__(self, **kwargs):
        super(SquareLabel, self).__init__(**kwargs)
        with self.canvas.before:
            # Set the background color here
            Color(0, 0, 0, 1)  # RGBA values (black)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    # def on_size(self, *args):
    #     self.rect.size = self.size
    #     self.rect.pos = self.pos

class NumTextInput(TextInput):
    def insert_text(self,substring,from_undo=False):
        nums = '1234567890'
        if len(self.text)==1 or not substring in nums:
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
class Game(BoxLayout):
    def __init__(self,**kwargs):
        super(Game, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.game_started = False
        self.game_bd = None
        self.btn = Button(text = "Start")
        self.btn.bind(on_press = self.start_game)
        self.add_widget(self.btn)
        self.tb = {}
        self.filled = 0
        self.game = None
        self.empties = 0

    def Victory(self,*args):
        self.rows = 11
        self.cols = 12
        self.game_started = False
        self.game_bd = None
        self.clear_widgets()
        self.btn = Button(text = "Start")
        self.btn.bind(on_press = self.start_game)
        self.add_widget(self.btn)
        self.tb = {}
        self.filled = 0
        self.game = None
        self.empties = 0
        App.get_running_app().screen_manager.current = 'Victory'

    def reset(self,*args):
        self.game = self.game_bd
        self.filled = 0

        for i in self.tb:
            i.text = ''
        
    def change_bd(self,*args):
        coords = self.tb[args[0]]
        self.game[coords[0]][coords[1]] = args[1]
        if args[1] == '':
            self.filled -= 1
        else:
            self.filled += 1
        if self.filled == self.empties:
            if isValidSudoku(self.game):
                self.Victory()

    def start_game(self,*args):
        self.boxes = []
        for i in range(11):
            if i!=3 and i!=7:
                b = BoxLayout(
                    orientation = 'vertical'
                )
            else:
                b = SquareLabel(
                    size_hint = (.05,1)
                )
            self.add_widget(b)
            self.boxes.append(b)
        self.game_reset = Button(text="Reset board")
        self.game_reset.bind(on_press=self.reset)
        self.add_widget(self.game_reset)
        
        bd = [['.' for i in range(9)] for i in range(9)]
        nums = [str(i) for i in range(1,10)]
        nums2 = nums[:]

        for c,i in enumerate(bd):
            r = randint(0,len(nums)-1)
            rand_num = randint(0,len(nums2)-1)
            cc = 0
            while nums2[rand_num] == nums[r] and cc<1000:
                rand_num = randint(0,len(nums2)-1)
                cc += 1
            bd[c][randint(3,8)] = nums.pop(r)
            bd[c][0] = nums2.pop(rand_num)

        bd = solveSudoku(bd)
        self.game_bd = bd[:]
        for i in bd:
            print(i)

        for c in range(len(self.game_bd)):

            for n in range(4):
                self.game_bd[c][randint(0,8)] = '.'

        self.remove_widget(self.btn)

        for c,i in enumerate(self.game_bd):
            # if c%3 == 0:
            #     if c != 8 and c >0:
            #         for ii in range(12):
            #             line = SquareLabel(height = 10,width=100)
            #             self.add_widget(line)

            for n,j in enumerate(i):
                if c%3 == 0 and c>0 and c<8:
                    line = SquareLabel(size_hint = (1,.05))
                    self.boxes[n + n//3].add_widget(line)
                if j == '.':
                    self.empties += 1
                    box = NumTextInput(background_color = [1,1,1,1],font_size = 20, multiline=False, size_hint = (1,1), padding=10)
                    self.tb[box] = [c,n]
                    box.bind(text=self.change_bd)
                else:
                    box = ColorLabel(text = j, color = [0,0,0,1],padding=10)
                self.boxes[n + n//3].add_widget(box)
        self.game = self.game_bd[:]

#third page
class Win(GridLayout):
    def __init__(self,**kwargs):
        super(Win, self).__init__(**kwargs)
        self.rows = 3
        self.cols = 1
        lbl = Label(text = 'You win!')
        self.add_widget(lbl)
        btn = Button(text = "Play again")
        btn.bind(on_press=self.switch)
        self.add_widget(btn)
        quit = Button(text = 'Exit')
        quit.bind(on_press = self.exit)
        self.add_widget(quit)

    def exit(self,*args):
        App.get_running_app().stop()

    def switch(self,*args):
        App.get_running_app().screen_manager.current = 'Second'

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
        
        self.thirdpage = Win()
        screen = Screen(name='Victory')
        screen.add_widget(self.thirdpage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == "__main__":
    MyApp().run()