from reedsolo import RSCodec

# Official block and EC specifications for QR Code Version 8



def get_qr_version8_block_ec(message_bytes: bytes, ec_level: str, target_block_index: int) -> bytes:
    """
    Computes the error correction codewords for a specific block of a Version 8 QR code.

    Parameters:
    - message_bytes (bytes): The full sequential stream of encoded data codewords.
    - ec_level (str): Error correction level ('L', 'M', 'Q', or 'H').
    - target_block_index (int): 0-indexed position of the block across all groups.

    Returns:
    - bytes: The Reed-Solomon error correction codewords for the specified block.
    """
    ec_level = ec_level.upper()
    if ec_level not in VERSION_8_SPECS:
        raise ValueError(f"Invalid EC level '{ec_level}'. Choose from 'L', 'M', 'Q', 'H'.")

    spec = VERSION_8_SPECS[ec_level]
    ec_per_block = spec['ec_per_block']

    # 1. Split the continuous message byte stream into individual blocks based on Version 8 rules
    all_blocks = []
    current_index = 0

    for group in spec['groups']:
        num_blocks = group['num_blocks']
        data_per_block = group['data_per_block']
        for _ in range(num_blocks):
            block_data = message_bytes[current_index: current_index + data_per_block]
            if len(block_data) < data_per_block:
                raise ValueError("Message bytes length is shorter than required for Version 8 at this EC level.")
            all_blocks.append(block_data)
            current_index += data_per_block

    if target_block_index < 0 or target_block_index >= len(all_blocks):
        raise IndexError(
            f"Target block index {target_block_index} out of range. Total blocks for {ec_level}: {len(all_blocks)}.")

    # 2. Select the target block data
    target_block = all_blocks[target_block_index]

    # 3. Initialize Reed-Solomon codec for the block
    rs = RSCodec(ec_per_block)

    # rs.encode appends parity bytes to the data array: returns (data + ec_codewords)
    encoded = rs.encode(target_block)
    ec_codewords = encoded[len(target_block):]

    return bytes(ec_codewords)


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Choose error correction level 'H' (High)
    chosen_ec_level = 'H'

    # Version 8-H has 4 blocks of 14 bytes + 2 blocks of 15 bytes = 86 total data codewords.
    total_data_codewords_needed = 86

    # Create a mock sequential string/byte array representing your encoded message data
    mock_message_stream = bytes([i % 256 for i in range(total_data_codewords_needed)])

    # Let's get the error correction codewords for Block 0
    block_index = 0
    ec_result = get_qr_version8_block_ec(mock_message_stream, chosen_ec_level, block_index)

    print(f"Version 8-{chosen_ec_level} | Block {block_index}")
    print(f"Number of EC codewords: {len(ec_result)}")
    print(f"EC Codewords (Decimal): {list(ec_result)}")