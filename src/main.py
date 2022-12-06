import os

from view import View

if __name__ == '__main__':
    os.system('clear')
    view = View()
    while True:
        view.loop()
