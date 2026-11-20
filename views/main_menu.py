import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
import utils.view_settings as vs
import os
from controllers.codify_controller import CodifyController
from controllers.decodify_controller import DecodifyController


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
    decodify_frame: ctk.CTkFrame
    decodify_label: ctk.CTkLabel
    decodify_input_label: ctk.CTkLabel
    decodify_input_entry: ctk.CTkEntry
    decodify_level_combo_box: ctk.CTkComboBox
    damage_input_label: ctk.CTkLabel
    damage_input_entry: ctk.CTkEntry
    damage_type_combo_box: ctk.CTkComboBox
    decodify_qr_button: ctk.CTkButton
    return_from_decodify_button: ctk.CTkButton
    error_decodify_label: ctk.CTkLabel
    result_decodify_label: ctk.CTkLabel
    codify_buttons_frame: ctk.CTkFrame
    decodify_buttons_frame: ctk.CTkFrame
    scale_factor: float
    resize_job: str | None
    scaled_fonts: list[tuple[ctk.CTkFont, int]]
    scaled_sizes: list[tuple]


    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")

        super().__init__()

        self.scale_factor = 1.0
        self.resize_job = None
        self.scaled_fonts = []
        self.scaled_sizes = []

        self.configure_window()
        self.create_widgets()
        self.place_widgets()
        self.after(200, self.refresh_scale)


    def configure_window(self) -> None:
        self.title(vs.WINDOW_TITLE)

        window_scaling: float = self.get_window_scaling()
        width: int = min(vs.BASE_WIDTH, int(self.winfo_screenwidth() / window_scaling * 0.9))
        height: int = min(vs.BASE_HEIGHT, int(self.winfo_screenheight() / window_scaling * 0.85))

        self.geometry(f"{width}x{height}")
        self.minsize(vs.MIN_WIDTH, vs.MIN_HEIGHT)
        self.resizable(vs.IS_RESIZABLE, vs.IS_RESIZABLE)
        self.configure(fg_color=vs.BACKGROUND_COLOR)

        self.scale_factor = self.compute_scale(width, height)
        self.bind("<Configure>", self.on_window_resize)


    def get_window_scaling(self) -> float:
        get_scaling = getattr(self, "_get_window_scaling", None)
        scaling: float = get_scaling() if get_scaling else self.winfo_fpixels("1i") / 96

        return scaling if scaling > 0 else 1.0


    def compute_scale(self, width: float, height: float) -> float:
        scale: float = min(width / vs.BASE_WIDTH, height / vs.BASE_HEIGHT)

        return max(0.35, min(1.6, scale))


    def scaled(self, value: int) -> int:
        return max(1, round(value * self.scale_factor))


    def make_font(self, family: str, size: int) -> ctk.CTkFont:
        font: ctk.CTkFont = ctk.CTkFont(family, size=self.scaled(size))
        self.scaled_fonts.append((font, size))

        return font


    def apply_sizes(self) -> None:
        for font, base_size in self.scaled_fonts:
            font.configure(size=self.scaled(base_size))

        for widget, base_width, base_height in self.scaled_sizes:
            widget.configure(width=self.scaled(base_width), height=self.scaled(base_height))


    def on_window_resize(self, event) -> None:
        if event.widget is not self:
            return

        if self.resize_job is not None:
            self.after_cancel(self.resize_job)

        self.resize_job = self.after(150, self.refresh_scale)


    def visible_frame(self) -> ctk.CTkFrame:
        for frame in (self.main_menu_frame, self.codify_frame, self.decodify_frame):
            if frame.winfo_manager():
                return frame

        return self.main_menu_frame


    def refresh_scale(self) -> None:
        self.resize_job = None

        if self.winfo_height() <= 1:
            return

        window_scaling: float = self.get_window_scaling()

        self.scale_factor = self.compute_scale(
            self.winfo_width() / window_scaling,
            self.winfo_height() / window_scaling
        )
        self.apply_sizes()
        self.layout_widgets()
        self.fit_to_window()


    def fit_to_window(self) -> None:
        self.update_idletasks()

        frame: ctk.CTkFrame = self.visible_frame()
        available_width: int = self.winfo_width()
        available_height: int = self.winfo_height()

        if available_height <= 1:
            return

        for _ in range(4):
            ratio: float = min(
                available_width / max(1, frame.winfo_reqwidth()),
                available_height / max(1, frame.winfo_reqheight())
            )

            if ratio >= 1:
                break

            self.scale_factor = max(0.3, self.scale_factor * ratio * 0.97)
            self.apply_sizes()
            self.layout_widgets()
            self.update_idletasks()


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
            font=self.make_font("Silkscreen", 64),
            fg_color="transparent",
            text_color=vs.FONT_COLOR,
            hover_color=vs.HOVER_COLOR,
            border_width=2,
            border_color=vs.FONT_COLOR,
            width=400,
            height=75,
            command=self.on_codify_button_click
        )
        self.decodify_button = ctk.CTkButton(
            master=self.main_menu_frame,
            text="Decodificar",
            font=self.make_font("Silkscreen", 64),
            fg_color="transparent",
            text_color=vs.FONT_COLOR,
            hover_color=vs.HOVER_COLOR,
            border_width=2,
            border_color=vs.FONT_COLOR,
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
            font=self.make_font("Silkscreen", 32),
            text_color=vs.FONT_COLOR
        )
        self.codify_input_entry = ctk.CTkEntry(
            master=self.codify_frame,
            font=self.make_font("Segoe UI", 32),
            width=700,
            height=75,
        )
        self.codify_label = ctk.CTkLabel(
            master=self.codify_frame,
            text="Codificar",
            font=self.make_font("Silkscreen", 72),
            text_color=vs.FONT_COLOR,
            width=400,
            height=75,
        )
        self.correction_level_input_label = ctk.CTkLabel(
            master=self.codify_frame,
            text="Seleccione el nivel de correccion",
            font=self.make_font("Silkscreen", 32),
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
            font=self.make_font("Silkscreen", 32),
            dropdown_font=self.make_font("Silkscreen", 32),
        )
        self.codify_buttons_frame = ctk.CTkFrame(
            master=self.codify_frame,
            fg_color="transparent"
        )
        self.codify_qr_button = ctk.CTkButton(
            master=self.codify_buttons_frame,
            text="Codificar Qr",
            font=self.make_font("Silkscreen", 40),
            fg_color="transparent",
            text_color=vs.FONT_COLOR,
            hover_color=vs.HOVER_COLOR,
            border_width=2,
            border_color=vs.FONT_COLOR,
            width=300,
            height=75,
            command=self.on_codify_qr_button_click
        )
        self.return_from_codify_button = ctk.CTkButton(
            master=self.codify_buttons_frame,
            text="Retornar",
            font=self.make_font("Silkscreen", 32),
            fg_color="transparent",
            text_color=vs.FONT_COLOR,
            hover_color=vs.HOVER_COLOR,
            border_width=2,
            border_color=vs.FONT_COLOR,
            width=200,
            height=75,
            command=self.on_return_from_codify_button_click
        )
        self.error_codify_label = ctk.CTkLabel(
            master=self.codify_frame,
            text="",
            font=self.make_font("Silkscreen", 16),
            text_color=vs.ERROR_COLOR
        )
        self.decodify_frame = ctk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        self.decodify_label = ctk.CTkLabel(
            master=self.decodify_frame,
            text="Decodificar",
            font=self.make_font("Silkscreen", 64),
            text_color=vs.FONT_COLOR,
        )
        self.decodify_input_label = ctk.CTkLabel(
            master=self.decodify_frame,
            text="Texto del Qr y nivel de correccion",
            font=self.make_font("Silkscreen", 32),
            text_color=vs.FONT_COLOR
        )
        self.decodify_input_entry = ctk.CTkEntry(
            master=self.decodify_frame,
            font=self.make_font("Segoe UI", 32),
            width=700,
            height=75,
        )
        self.decodify_level_combo_box = ctk.CTkComboBox(
            master=self.decodify_frame,
            values=["L", "M", "Q", "H"],
            width=400,
            height=75,
            state="readonly",
            font=self.make_font("Silkscreen", 32),
            dropdown_font=self.make_font("Silkscreen", 32),
        )
        self.damage_input_label = ctk.CTkLabel(
            master=self.decodify_frame,
            text="Porcentaje de dano (0 a 100) y tipo",
            font=self.make_font("Silkscreen", 32),
            text_color=vs.FONT_COLOR
        )
        self.damage_input_entry = ctk.CTkEntry(
            master=self.decodify_frame,
            font=self.make_font("Segoe UI", 32),
            width=400,
            height=75,
        )
        self.damage_type_combo_box = ctk.CTkComboBox(
            master=self.decodify_frame,
            values=["Aleatorio", "Mancha"],
            width=400,
            height=75,
            state="readonly",
            font=self.make_font("Silkscreen", 32),
            dropdown_font=self.make_font("Silkscreen", 32),
        )
        self.decodify_buttons_frame = ctk.CTkFrame(
            master=self.decodify_frame,
            fg_color="transparent"
        )
        self.decodify_qr_button = ctk.CTkButton(
            master=self.decodify_buttons_frame,
            text="Decodificar Qr",
            font=self.make_font("Silkscreen", 40),
            fg_color="transparent",
            text_color=vs.FONT_COLOR,
            hover_color=vs.HOVER_COLOR,
            border_width=2,
            border_color=vs.FONT_COLOR,
            width=300,
            height=75,
            command=self.on_decodify_qr_button_click
        )
        self.return_from_decodify_button = ctk.CTkButton(
            master=self.decodify_buttons_frame,
            text="Retornar",
            font=self.make_font("Silkscreen", 32),
            fg_color="transparent",
            text_color=vs.FONT_COLOR,
            hover_color=vs.HOVER_COLOR,
            border_width=2,
            border_color=vs.FONT_COLOR,
            width=200,
            height=75,
            command=self.on_return_from_decodify_button_click
        )
        self.error_decodify_label = ctk.CTkLabel(
            master=self.decodify_frame,
            text="",
            font=self.make_font("Silkscreen", 16),
            text_color=vs.ERROR_COLOR
        )
        self.result_decodify_label = ctk.CTkLabel(
            master=self.decodify_frame,
            text="",
            font=self.make_font("Silkscreen", 32),
            text_color=vs.FONT_COLOR
        )

        self.scaled_sizes = [
            (self.codify_button, 560, 90),
            (self.decodify_button, 560, 90),
            (self.codify_input_entry, 700, 70),
            (self.codify_label, 500, 90),
            (self.correction_level_input_label, 400, 60),
            (self.correction_level_combo_box, 400, 70),
            (self.codify_qr_button, 460, 75),
            (self.return_from_codify_button, 240, 75),
            (self.decodify_input_entry, 700, 60),
            (self.decodify_level_combo_box, 400, 60),
            (self.damage_input_entry, 400, 60),
            (self.damage_type_combo_box, 400, 60),
            (self.decodify_qr_button, 520, 75),
            (self.return_from_decodify_button, 240, 75),
        ]
        self.apply_sizes()


    def place_widgets(self) -> None:
        self.main_menu_frame.pack(fill="both", expand=True)
        self.layout_widgets()


    def layout_widgets(self) -> None:
        s = self.scaled

        self.main_title.pack(pady=(s(40), s(20)))
        self.codify_button.pack(pady=(s(120), s(20)))
        self.decodify_button.pack(pady=(s(60), s(20)))

        self.codify_buttons_frame.pack(side="bottom", pady=(s(10), s(30)))
        self.error_codify_label.pack(side="bottom")
        self.codify_label.pack(pady=(s(30), s(10)))
        self.codify_input_label.pack(pady=(s(30), s(10)))
        self.codify_input_entry.pack()
        self.correction_level_input_label.pack(pady=(s(25), s(10)))
        self.correction_level_combo_box.pack()
        self.return_from_codify_button.pack(side="left", padx=s(20))
        self.codify_qr_button.pack(side="left", padx=s(20))

        self.decodify_buttons_frame.pack(side="bottom", pady=(s(10), s(30)))
        self.result_decodify_label.pack(side="bottom", pady=(s(5), s(5)))
        self.error_decodify_label.pack(side="bottom")
        self.decodify_label.pack(pady=(s(30), s(10)))
        self.decodify_input_label.pack(pady=(s(20), s(10)))
        self.decodify_input_entry.pack()
        self.decodify_level_combo_box.pack(pady=(s(15), 0))
        self.damage_input_label.pack(pady=(s(25), s(10)))
        self.damage_input_entry.pack()
        self.damage_type_combo_box.pack(pady=(s(15), 0))
        self.return_from_decodify_button.pack(side="left", padx=s(20))
        self.decodify_qr_button.pack(side="left", padx=s(20))


    def on_codify_button_click(self) -> None:
        self.main_menu_frame.pack_forget()
        self.codify_frame.pack(fill="both", expand=True)
        self.refresh_scale()


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
        self.refresh_scale()


    def on_decodify_button_click(self) -> None:
        self.main_menu_frame.pack_forget()
        self.decodify_frame.pack(fill="both", expand=True)
        self.refresh_scale()


    def on_decodify_qr_button_click(self) -> None:
        message: str = self.decodify_input_entry.get()
        level_of_correction: str = self.decodify_level_combo_box.get()
        damage_type: str = self.damage_type_combo_box.get()

        try:
            damage_percentage: float = float(self.damage_input_entry.get().replace(",", "."))
        except ValueError:
            damage_percentage = -1

        if not 0 <= damage_percentage <= 100:
            self.error_decodify_label.configure(
                text="El porcentaje de dano debe ser un numero entre 0 y 100"
            )
            self.result_decodify_label.configure(text="")
            return

        decodify_controller: DecodifyController = DecodifyController(message, level_of_correction)

        if decodify_controller.determine_errors():
            self.error_decodify_label.configure(
                text="Texto invalido o excede los limites de este nivel de corrreccion"
            )
            self.result_decodify_label.configure(text="")
            return

        self.error_decodify_label.configure(
            text=""
        )
        damaged_matrix: np.ndarray = decodify_controller.damage_qr(damage_percentage, damage_type)
        decoded_message: str | None = decodify_controller.decode_qr()

        if decoded_message is None:
            self.result_decodify_label.configure(
                text="No se pudo decodificar el Qr",
                text_color=vs.ERROR_COLOR
            )
        else:
            self.result_decodify_label.configure(
                text=f"Mensaje recuperado: {decoded_message}",
                text_color=vs.FONT_COLOR
            )

        figure, axes = plt.subplots(1, 2)
        for axis, matrix, title in zip(
                axes,
                [decodify_controller.original_matrix, damaged_matrix],
                ["Original", f"Danado {damage_percentage:g}%"]
        ):
            axis.imshow(
                matrix == 1,
                cmap="gray_r",
                vmin=0,
                vmax=1,
                interpolation="nearest"
            )
            axis.set_title(title)
            axis.axis("off")
        plt.show()


    def on_return_from_decodify_button_click(self) -> None:
        self.decodify_frame.pack_forget()
        self.result_decodify_label.configure(text="")
        self.error_decodify_label.configure(text="")
        self.main_menu_frame.pack(fill="both", expand=True)
        self.refresh_scale()


    def _setup_fonts(self) -> None:
        current_dir: str = os.path.dirname(os.path.abspath(__file__))
        root_dir: str = os.path.dirname(current_dir)
        font_path: str = os.path.join(root_dir, "assets", "main_font.ttf")

        if not os.path.exists(font_path):
            print(f"Advertencia: no se encontró la fuente en {font_path}")

        try:
            self.custom_font = self.make_font("Silkscreen", 64)
        except Exception:
            self.custom_font = self.make_font("Arial", 64)


window: MainWindow = MainWindow()
window.mainloop()