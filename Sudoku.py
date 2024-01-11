from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from sudoku_solver import solveSudoku,isValidSudoku
from random import randint
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

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
        app.screen_manager.current = 'Second'

#page 2
class game(BoxLayout):
    def __init__(self,**kwargs):
        super(game, self).__init__(**kwargs)
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
        game_bd = bd[:]
        for c in range(len(game_bd)):
            for n in range(4):
                game_bd[c][randint(0,8)] = '.'

class app(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.firstpage = Sudoku()
        screen = Screen(name='First')
        screen.add_widget(self.firstpage)
        self.screen_manager.add_widget(screen)

        self.secondpage = game()
        screen = Screen(name='Second')
        screen.add_widget(self.secondpage)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager
    
if __name__ == "__main__":
    app().run()