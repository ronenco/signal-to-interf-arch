import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hardware_sim.fft_block import FftBlock
from hardware_sim.register_map import FFtRegisterMap
from hardware_sim.buffer import Buffer
from general.helper_functions import create_fft_config, generate_single_tone, get_fft_size
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

if __name__ == "__main__":
    test_fft_block_reg_map()
    test_fft_block()
    print("All tests passed!")
