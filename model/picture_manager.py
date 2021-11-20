from PIL import ImageTk, Image, ImageFilter


class PictureManager:
    def resize_image(self, image: Image.Image, width=400, height=400) -> Image.Image:
        return image.resize((width, height))

    def open(self, file_path):
        return Image.open(file_path)

    def convert_to_photo_image(self, image):
        return ImageTk.PhotoImage(image)

    def emboss_image(self, image: Image.Image) -> Image.Image:
        ImageFilter.EMBOSS.filterargs = ((3, 3), 1, 128, (-1, 0, 0, 0, 1, 0, 0, 0, 0))
        return image.filter(ImageFilter.EMBOSS)

    def thumbnail_image(self, image: Image.Image, width=400, height=400) -> None:
        image.thumbnail((width, height), Image.ANTIALIAS)
