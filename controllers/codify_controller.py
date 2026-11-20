from encoder import Encoder
import numpy as np


class CodifyController:


    encoder: Encoder


    def __init__(self, message: str, correction_level: str) -> None:
        self.encoder = Encoder(message, correction_level)


    def determine_errors(self) -> bool:
        if self.encoder.encode_string_text() == -1:
            return True

        return False


    def show_qr(self) -> np.ndarray:
        matrix: np.ndarray = self.encoder.final_matrix_output()

        return matrix

