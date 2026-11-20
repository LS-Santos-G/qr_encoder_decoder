from encoder import Encoder, qr_specs
from decoder import decode_matrix
import channel
import numpy as np


class DecodifyController:


    encoder: Encoder
    original_matrix: np.ndarray
    damaged_matrix: np.ndarray


    def __init__(self, message: str, correction_level: str) -> None:
        self.encoder = Encoder(message, correction_level)
        self.message = message
        self.correction_level = correction_level


    def determine_errors(self) -> bool:
        if any(ord(char) > 255 for char in self.message):
            return True

        if self.encoder.encode_string_text() == -1:
            return True

        return False


    def damage_qr(self, damage_percentage: float, damage_type: str) -> np.ndarray:
        self.original_matrix = self.encoder.final_matrix_output()
        fraction: float = damage_percentage / 100

        if damage_type == "Mancha":
            self.damaged_matrix = channel.burst(self.original_matrix, fraction)
        else:
            self.damaged_matrix = channel.flip_exact(self.original_matrix, fraction)

        return self.damaged_matrix


    def decode_qr(self) -> str | None:
        return decode_matrix(self.damaged_matrix)
