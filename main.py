from view import main_window
from model import picture_manager


def main(name):
    pic_manager = picture_manager.PictureManager()
    w = main_window.MainWindow(pic_manager)
    w.open()


if __name__ == '__main__':
    main('PyCharm')
