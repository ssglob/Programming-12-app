from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from sudoku_solver import Solution

class Sudoku(App):
    def build(self):
        self.window = StackLayout()
        self.start_game = Button(
            text = "Generate game",
            color = '#ffffff'
        )
        self.start_game.bind(on_press = self.game)
        self.window.add_widget(self.start_game)
    def game(self,event):
        pass

if __name__ == "__main__":
    Sudoku().run()