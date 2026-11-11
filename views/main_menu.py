import customtkinter as ctk
import utils.view_settings as vs
from PIL import Image


class MainWindow(ctk.CTk):


    squares: list[tuple[int, int, str, bool]] = [
        (30, 30, "filled", False),
        (60, 30, "empty", False),
        (90, 30, "filled", True),
    ]
    full_square_image: Image.Image = Image.open("../assets/full_square.png").convert("RGB")
    hollow_square_image: Image.Image = Image.open("../assets/hollow_square.png").convert("RGB")



    def __init__(self) -> None:
        super().__init__()

        self.configure_window()



    def configure_window(self) -> None:
        self.title(vs.WINDOW_TITLE)
        self.geometry(vs.RESOLUTION)
        self.resizable(vs.IS_RESIZABLE,  vs.IS_RESIZABLE)
        self.configure(fg_color=vs.BACKGROUND_COLOR)






window: MainWindow = MainWindow()
window.mainloop()