from tkinter import *
from ctypes import windll
from tkinter import filedialog
from PIL import Image, ImageTk
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

        self._emboss_applied = False

        # main frame located in window
        self._program_frame = Frame(window)

        # frame with buttons and dropdowns
        self._controls_frame = Frame(self._program_frame)

        # main label
        # packing means attaching to the frame
        self._main_label = Label(self._controls_frame, font=('Arial', 14), text='Python image converter')
        self._main_label.pack(fill="both", expand=1)

        # keep aspect ration flag
        self._aspect_ration_value = IntVar()
        self._aspect_ratio = Checkbutton(self._controls_frame, text="Aspect ratio", variable=self._aspect_ration_value)
        self._aspect_ratio.pack()

        # user's height entry
        self._height_entry_label = Label(self._controls_frame, text="Height")
        self._height_entry_label.pack(side=TOP)
        self._height_entry = Entry(self._controls_frame)
        self._height_entry.pack(side=TOP, pady=10)

        # user's width entry
        self._width_entry_label = Label(self._controls_frame, text="Width")
        self._width_entry_label.pack(side=TOP)
        self._width_entry = Entry(self._controls_frame)
        self._width_entry.pack(side=TOP, pady=10)

        self.register_download_png_button(self._controls_frame)
        self.register_download_bmp_button(self._controls_frame)
        self.register_emboss_button(self._controls_frame)

        # modified picture
        self._modified_picture = Label(self._program_frame)
        self._modified_picture.pack(side=RIGHT)

        # Create uploaded picture Image
        self._uploaded_picture = Label(self._program_frame)
        self._uploaded_picture.pack(side=LEFT)

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

        self._emboss_applied = False

    def download_base_handler(self, image_format='png'):
        if not getattr(self, '_file_path', None):
            return

        save_path = filedialog.asksaveasfilename()

        if not save_path:
            return

        height = self._height_entry.get()
        width = self._width_entry.get()

        if height and width:

            base_image = self._image

            if self._aspect_ration_value.get():
                self._picture_manager.thumbnail_image(base_image, int(width), int(height))
            else:
                base_image = self._picture_manager.resize_image(base_image, int(width), int(height))

            base_image.save(save_path, format=image_format)
            return

        self._image.save(save_path, format=image_format)

    def download_button_png_handler(self):
        self.download_base_handler('png')

    def download_button_bmp_handler(self):
        self.download_base_handler('bmp')

    def emboss_button_handler(self):
        if not getattr(self, '_file_path', None):
            return

        self._image = self._picture_manager.emboss_image(self._image)

        resized = self._picture_manager.resize_image(self._image)

        pi = self._picture_manager.convert_to_photo_image(resized)

        self._modified_picture.config(image=pi)
        self._modified_picture.image = pi

        self._emboss_applied = True

    def register_download_png_button(self, frame):
        self._download_png_button = Button(frame, text='Download png',
                                           command=self.download_button_png_handler)
        self._download_png_button.pack(side=BOTTOM, pady=10)

    def register_emboss_button(self, frame):
        self._emboss_button = Button(frame, text='Apply emboss',
                                     command=self.emboss_button_handler)
        self._emboss_button.pack(side=BOTTOM, pady=10)

    def register_download_bmp_button(self, frame):
        self._download_bmp_button = Button(frame, text='Download bmp',
                                           command=self.download_button_bmp_handler)
        self._download_bmp_button.pack(side=BOTTOM, pady=10)

    def register_upload_button(self, frame):
        self._upload_button = Button(frame, text='Upload image',
                                     command=self.upload_button_click_handler)
        self._upload_button.pack(side=BOTTOM, pady=10)
