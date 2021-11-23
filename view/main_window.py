from tkinter import *
from ctypes import windll
from tkinter import filedialog
from model.picture_manager import PictureManager


class MainWindow:
    def __init__(self, picture_manager: PictureManager):
        window = Tk()
        windll.shcore.SetProcessDpiAwareness(1)

        window.title('Python images converter')
        window.geometry('1280x720')
        window.resizable(width=TRUE, height=TRUE)

        self._window = window
        self._picture_manager = picture_manager

        self._brightness_applied = False

        # main frame located in window
        self._program_frame = Frame(window)

        # frame with buttons and dropdowns
        self._controls_frame = Frame(self._program_frame)

        # main label
        # packing means attaching to the frame
        self._main_label = Label(self._controls_frame, font=('Arial', 14), text='Python image converter')
        self._main_label.pack(fill="both", expand=1)

        # user's brightness entry
        self._brightness_entry_label = Label(self._controls_frame, text="Brightness")
        self._brightness_entry_label.pack(side=TOP)
        self._brightness_entry = Entry(self._controls_frame)
        self._brightness_entry.pack(side=TOP, pady=10)

        self.register_download_png_button(self._controls_frame)
        self.register_download_jpeg_button(self._controls_frame)
        self.register_brightness_button(self._controls_frame)

        # modified picture
        self._modified_picture = Label(self._program_frame, borderwidth=5, fg="gray", relief="raised")
        self._modified_picture.pack(side=RIGHT, padx=20)

        # Create uploaded picture Image
        self._uploaded_picture = Label(self._program_frame, borderwidth=5, fg="gray", relief="raised")
        self._uploaded_picture.pack(side=LEFT, padx=20)

        # mount mane frame
        self._program_frame.pack(fill="both", expand=1, pady=10)
        self._program_frame.focus_set()

        self.register_upload_button(self._controls_frame)

        # mount controls frame
        self._controls_frame.pack(fill=Y, expand=1)

    def open(self):
        self._window.mainloop()

    def upload_button_click_handler(self):
        self._file_path = filedialog.askopenfilename()

        if not getattr(self, '_file_path', None):
            return

        self._image = self._picture_manager.open(self._file_path)

        resized_image = self._picture_manager.resize_image(self._image)
        photo_image = self._picture_manager.convert_to_photo_image(resized_image)

        # original_image = Image
        self._uploaded_picture.config(image=photo_image)
        self._uploaded_picture.image = photo_image

        self._modified_picture.config(image=photo_image)
        self._modified_picture.image = photo_image

        self._brightness_applied = False

    def download_base_handler(self, image_format='png'):
        if not getattr(self, '_file_path', None):
            return

        save_path = filedialog.asksaveasfilename()

        if not save_path:
            return

        self._picture_manager.save_image(save_path, self._image, image_format)

    def download_button_png_handler(self):
        self.download_base_handler('png')

    def download_button_jpeg_handler(self):
        self.download_base_handler('jpeg')

    def brightness_button_handler(self):
        if not getattr(self, '_file_path', None):
            return

        brightness = self._brightness_entry.get()

        if brightness:
            self._image = self._picture_manager.brighten_image(self._image, float(brightness))

        resized = self._picture_manager.resize_image(self._image)

        pi = self._picture_manager.convert_to_photo_image(resized)

        self._modified_picture.config(image=pi)
        self._modified_picture.image = pi

        self._brightness_applied = True

    def register_download_png_button(self, frame):
        self._download_png_button = Button(frame, text='Download png',
                                           command=self.download_button_png_handler, height=2, width=30, bg='gray')
        self._download_png_button.pack(side=BOTTOM, pady=10)

    def register_brightness_button(self, frame):
        self._brighten_button = Button(frame, text='Apply brightness',
                                       command=self.brightness_button_handler, height=2, width=30, bg='gray')
        self._brighten_button.pack(side=BOTTOM, pady=10)

    def register_download_jpeg_button(self, frame):
        self._download_jpeg_button = Button(frame, text='Download jpeg',
                                            command=self.download_button_jpeg_handler, height=2, width=30, bg='gray')
        self._download_jpeg_button.pack(side=BOTTOM, pady=10)

    def register_upload_button(self, frame):
        self._upload_button = Button(frame, text='Upload image',
                                     command=self.upload_button_click_handler, height=2, width=30, bg='gray')
        self._upload_button.pack(side=BOTTOM, pady=10)
