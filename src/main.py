import os
import subprocess
import tkinter as tk


CALL_TYPE = 'EXE'


class SelectWindow(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.snake_btn = tk.Button(self, text='Snake', command=lambda: app.play('snake'))
        self.snake_btn.pack(expand=True, ipadx=100)

        self.pacman_btn = tk.Button(self, text='PacMan', command=lambda: app.play('pacman'))
        self.pacman_btn.pack(expand=True, ipadx=100)

        self.astroid_btn = tk.Button(self, text='Astroids', command=lambda: app.play('astroids'))
        self.astroid_btn.pack(expand=True, ipadx=100)

        self.grid(row=0, column=0, sticky='nsew')


class ErrorWindow(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.label = tk.Label(self, text='Sorry... It looks like that game isn\'t avaliable at the moment')
        self.label.pack(expand=True, ipadx=200)

        self.back_btn = tk.Button(self, text='Go back', command=lambda: app.select_window.tkraise())
        self.back_btn.pack(expand=True, ipadx=200, pady=100)

        self.grid(row=0, column=0, sticky='nsew')


class Window(tk.Tk):
    def __init__(self):
        """
            An arcade app with a list of old arcade games 
            built in python
        """

        super().__init__()

        self.title('Arcade')

        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)

        self.select_window = SelectWindow(self.container, self)
        self.error_window  = ErrorWindow(self.container, self)

        self.select_window.tkraise()
        self.mainloop()

    def play(self, game: str):
        """
            Open a pygame app

            :param game: The name of the python file for the game
        """

        c_dir = os.getcwd()
        if os.path.exists(f'{c_dir}/{game}'):
            self.wm_state('iconic')

            if CALL_TYPE == 'EXE':
                subprocess.call([f'{c_dir}/{game}/{game}.exe'])
            else:
                os.system(f'python "{c_dir}/{game}/{game}.py"')
        else:
            raise Exception('Unimplemented game')
        
    def report_callback_exception(self, *args, **kwargs):
        self.error_window.tkraise()


if __name__ == '__main__':
    CALL_TYPE = 'PYTHON'
    path      = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)

    app = Window()
