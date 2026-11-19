import customtkinter as ctk
import utils.view_settings as vs
import os
from PIL import Image


class MainWindow(ctk.CTk):


    main_title: ctk.CTkLabel
    custom_font: ctk.CTkFont
    button_unpressed_image: ctk.CTkImage
    button_hover_image: ctk.CTkImage
    codify_button: ctk.CTkButton


    def __init__(self) -> None:
        super().__init__()

        self.configure_window()
        self.create_widgets()
        self.place_widgets()


    def configure_window(self) -> None:
        self.title(vs.WINDOW_TITLE)
        self.geometry(vs.RESOLUTION)
        self.resizable(vs.IS_RESIZABLE,  vs.IS_RESIZABLE)
        self.configure(fg_color=vs.BACKGROUND_COLOR)


    def create_widgets(self) -> None:
        self._setup_fonts()
        self._setup_sprite_sheet()

        self.main_title = ctk.CTkLabel(
            master=self,
            text="Codificador y Decodificador de Qrs",
            font=self.custom_font,
            text_color=vs.FONT_COLOR,
        )
        self.codify_button = ctk.CTkButton(
            master=self,
            text="Codificar",
            image=self.button_unpressed_image,
            fg_color="transparent",
            width=200,
            height=50,
            command=self.on_button_click
        )


    def place_widgets(self) -> None:
        self.main_title.pack(pady=(40, 20))
        self.codify_button.pack(pady=(100, 20))


    def on_button_click(self) -> None:
        pass


    def _setup_fonts(self) -> None:
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        root_dir: str = os.path.dirname(current_dir)
        font_path: str = os.path.join(current_dir, "assets", "main_font.ttf")

        if not os.path.exists(font_path):
            print(f"Advertencia: no se encontro la fuente en {font_path}")

        try:
            self.custom_font = ctk.CTkFont(family="Silkscreen", size=64)
        except Exception:
            self.custom_font = ctk.CTkFont(family="Arial", size=64)


    def _setup_sprite_sheet(self) -> None:
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        root_dir: str = os.path.dirname(current_dir)
        sprite_sheet_path: str = os.path.join(root_dir, "assets", "menu_buttons.png")

        sprite_sheet = Image.open(sprite_sheet_path)

        total_width, height = sprite_sheet.size
        half_width = int(total_width / 2)

        button_height, button_width = 392, 64

        img_normal_pil: Image.Image = sprite_sheet.crop((0, 0, half_width, height))
        img_pressed_pil: Image.Image = sprite_sheet.crop((half_width, 0, total_width, height))

        self.button_unpressed_image = ctk.CTkImage(
            light_image=img_normal_pil,
            dark_image=img_normal_pil,
            size=(button_height, button_width)
        )

        self.button_hover_image = ctk.CTkImage(
            light_image=img_pressed_pil,
            dark_image=img_pressed_pil,
            size=(button_height, button_width)
        )













window: MainWindow = MainWindow()
window.mainloop()