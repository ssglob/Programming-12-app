from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from sudoku_solver import Solution

class Sudoku(App):
    def build(self):
        self.window = BoxLayout(spacing = 20,orientation = "vertical")
        self.sudoku_image = Image(source='sudoku_image.jpg',size_hint = (1,.3),pos_hint = {'top':1})
        self.window.add_widget(self.sudoku_image)
        self.start_game = Button(text = "Generate game",font_size = 30,size_hint = (1,.3), pos_hint = {'center_y':1})
        self.start_game.bind(on_press = self.game)
        self.window.add_widget(self.start_game)
        return self.window
    def game(self,event):
        pass

if __name__ == "__main__":
    Sudoku().run()