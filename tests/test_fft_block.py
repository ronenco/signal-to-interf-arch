import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware_sim.fft_block import FftBlock
from hardware_sim.register_map import FFtRegisterMap
from hardware_sim.buffer import Buffer
import numpy as np
import math

def test_fft_block_reg_map():
    """
    Test the FFT block register map.
    """
    fft_register = FFtRegisterMap()

    fft_register.write_register("FFT_START", 1)
    assert fft_register.register_map["FFT_START"].value == 1

    value = fft_register.read_register("FFT_START")
    assert value == 1

    try:
        fft_register.write_register("FFT_DONE", 1)
    except PermissionError as e:
        print(f"Caught expected error: {e}")

    try:
        fft_register.write_register("FFT_DATA_IN", 2**32)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        fft_register.read_register("NON_EXISTENT")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        fft_register.write_register("NON_EXISTENT", 1)
    except ValueError as e:
        print(f"Caught expected error: {e}")

def test_fft_block():
    """
    Test the FFT block functionality.
    """
    fft_block = FftBlock()

    # Create a realistic config
    config = create_fft_config(fft_size_code=5, zero_padding=0, normalization=1, phase_correction=0, phase_sign=0)
    fft_block.configure(config)

    # Generate a single-tone signal
    input_data = generate_single_tone(frequency_bin=5, fft_size=64)
    fft_block.load_input(input_data)

    # Run the FFT block
    fft_block.run()

    # Check output
    output_data = fft_block.get_output()
    assert output_data is not None
    print("FFT Output Magnitudes:", np.abs(output_data))

# --- Helper Functions ---

def create_fft_config(fft_size_code, zero_padding, normalization, phase_correction, phase_sign):
    """
    Helper to create a 32-bit config word for the FFT block.
    """
    config = 0
    config |= (fft_size_code & 0xF)        # 4 bits for fft_size
    config |= (zero_padding & 0x3) << 4     # 2 bits for padding
    config |= (phase_correction & 0x7FF) << 6  # 11 bits for phase correction
    config |= (phase_sign & 0x1) << 17      # 1 bit for phase sign
    config |= (normalization & 0x1) << 18   # 1 bit for normalization
    return config

def generate_single_tone(frequency_bin, fft_size):
    """
    Helper to generate a single-tone complex sinusoid.
    """
    n = np.arange(fft_size) # Time indices (or sample indices)
    # Generate a complex sinusoid
    tone = np.exp(1j * 2 * np.pi * frequency_bin * n / fft_size)
    return tone

if __name__ == "__main__":
    test_fft_block_reg_map()
    test_fft_block()
