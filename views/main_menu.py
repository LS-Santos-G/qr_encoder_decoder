import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import utils.view_settings as vs
import os
from controllers.codify_controller import CodifyController


class MainWindow(ctk.CTk):


    main_title: ctk.CTkLabel
    custom_font: ctk.CTkFont
    codify_button: ctk.CTkButton
    main_menu_frame: ctk.CTkFrame
    codify_frame: ctk.CTkFrame
    decodify_button: ctk.CTkButton
    codify_input_label: ctk.CTkLabel
    codify_input_entry: ctk.CTkEntry
    codify_label: ctk.CTkLabel
    correction_level_input_label: ctk.CTkLabel
    correction_level_combo_box: ctk.CTkComboBox
    codify_qr_button: ctk.CTkButton
    return_from_codify_button: ctk.CTkButton
    error_codify_label: ctk.CTkLabel


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

        self.main_menu_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        self.main_title = ctk.CTkLabel(
            master=self.main_menu_frame,
            text="Codificador y Decodificador de Qrs",
            font=self.custom_font,
            text_color=vs.FONT_COLOR,
        )
        self.codify_button = ctk.CTkButton(
            master=self.main_menu_frame,
            text="Codificar",
            font=ctk.CTkFont("Silkscreen", size=64),
            fg_color="transparent",
            width=400,
            height=75,
            command=self.on_codify_button_click
        )
        self.decodify_button = ctk.CTkButton(
            master=self.main_menu_frame,
            text="Decodificar",
            font=ctk.CTkFont("Silkscreen", size=64),
            fg_color="transparent",
            width=400,
            height=75,
            command=self.on_decodify_button_click
        )
        self.codify_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        self.codify_input_label = ctk.CTkLabel(
            master=self.codify_frame,
            text="Escriba texto a codificar",
            font=ctk.CTkFont("Silkscreen", size=32),
            text_color=vs.FONT_COLOR
        )
        self.codify_input_entry = ctk.CTkEntry(
            master=self.codify_frame,
            font=ctk.CTkFont("Segoe UI", size=32),
            width=700,
            height=75,
        )
        self.codify_label = ctk.CTkLabel(
            master=self.codify_frame,
            text="Codificar",
            font=ctk.CTkFont("Silkscreen", size=128),
            text_color=vs.FONT_COLOR,
            width=400,
            height=75,
        )
        self.correction_level_input_label = ctk.CTkLabel(
            master=self.codify_frame,
            text="Seleccione el nivel de correccion",
            font=ctk.CTkFont("Silkscreen", size=32),
            text_color=vs.FONT_COLOR,
            width=400,
            height=75,
        )
        self.correction_level_combo_box = ctk.CTkComboBox(
            master=self.codify_frame,
            values=["L", "M", "Q", "H"],
            width=400,
            height=75,
            state="readonly",
            font=ctk.CTkFont("Silkscreen", size=32),
            dropdown_font=ctk.CTkFont("Silkscreen", size=32),
        )
        self.codify_qr_button = ctk.CTkButton(
            master=self.codify_frame,
            text="Codificar Qr",
            font=ctk.CTkFont("Silkscreen", size=64),
            fg_color="transparent",
            width=300,
            height=75,
            command=self.on_codify_qr_button_click
        )
        self.return_from_codify_button = ctk.CTkButton(
            master=self.codify_frame,
            text="Retornar",
            font=ctk.CTkFont("Silkscreen", size=32),
            fg_color="transparent",
            width=200,
            height=75,
            command=self.on_return_from_codify_button_click
        )
        self.error_codify_label = ctk.CTkLabel(
            master=self.codify_frame,
            text="",
            font=ctk.CTkFont("Silkscreen", size=16),
            text_color=vs.ERROR_COLOR
        )


    def place_widgets(self) -> None:
        self.main_menu_frame.pack(fill="both", expand=True)
        self.main_title.pack(pady=(40, 20))
        self.codify_button.pack(pady=(250, 20))
        self.decodify_button.pack(pady=(150, 20))

        self.codify_label.pack(pady=(100, 20))
        self.codify_input_label.pack(pady=(100, 20))
        self.codify_input_entry.pack()
        self.error_codify_label.pack(pady=(10, 0))
        self.correction_level_input_label.pack(pady=(25, 20))
        self.correction_level_combo_box.pack()
        self.codify_qr_button.pack(pady=(100, 50))
        self.return_from_codify_button.pack()


    def on_codify_button_click(self) -> None:
        self.main_menu_frame.pack_forget()
        self.codify_frame.pack(fill="both", expand=True)


    def on_codify_qr_button_click(self) -> None:
        message: str = self.codify_input_entry.get()
        level_of_correction: str = self.correction_level_combo_box.get()

        codify_controller: CodifyController = CodifyController(message, level_of_correction)

        if codify_controller.determine_errors():
            self.error_codify_label.configure(
                text="Texto excede los limites de este nivel de corrreccion"
            )
            return

        self.error_codify_label.configure(
            text=""
        )
        matrix: np.ndarray = codify_controller.show_qr()

        plt.imshow(
            matrix == 1,
            cmap="gray_r",
            vmin=0,
            vmax=1,
            interpolation="nearest"
        )
        plt.show()


    def on_return_from_codify_button_click(self) -> None:
        self.codify_frame.pack_forget()
        self.main_menu_frame.pack(fill="both", expand=True)


    def on_decodify_button_click(self) -> None:
        pass


    def _setup_fonts(self) -> None:
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        root_dir: str = os.path.dirname(current_dir)
        font_path: str = os.path.join(root_dir, "assets", "main_font.ttf")

        if not os.path.exists(font_path):
            print(f"Advertencia: no se encontró la fuente en {font_path}")

        try:
            self.custom_font = ctk.CTkFont(family="Silkscreen", size=64)
        except Exception:
            self.custom_font = ctk.CTkFont(family="Arial", size=64)


window: MainWindow = MainWindow()
window.mainloop()