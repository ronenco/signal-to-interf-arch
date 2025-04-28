# This script tests the cli controller for the FFT block
# TODO - add user input to the test (using unittest.mock)
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware_sim.fft_block import FftBlock
from hardware_sim.buffer import Buffer
from hardware_sim.register_map import FFtRegisterMap
from interface.cli_controller import run_fft_flow
from general.helper_functions import create_fft_config, generate_single_tone

def test_run_fft_flow():
    # Setup system
    register_map = FFtRegisterMap()
    fft_block = FftBlock()
    input_buffer = Buffer(4096, 4096)
    output_buffer = Buffer(4096, 4096)
    
    fft_block.bind_input_output(input_buffer, output_buffer)
    register_map.bind_module_to_register(fft_block, "FFT_START")
    register_map.bind_module_to_register(fft_block, "FFT_CONFIG")
    
    # Pre-load a dummy signal
    fft_size = 64
    signal = generate_single_tone(fft_size, 20)
    input_buffer.writeBuffer(signal)

    # Create a basic config
    config = create_fft_config(
        fft_size_code=5,  # Corresponds to 64 FFT points
        zero_padding=0,
        normalization=1,
        phase_correction=0,
        phase_sign=0
    )
    register_map.write_register("FFT_CONFIG", config)

    # Run FFT via the CLI helper
    run_fft_flow(register_map, fft_block)

    # Assertions
    output = output_buffer.getBuffer()
    assert output is not None, "Output buffer is empty after running FFT"
    assert len(output) == fft_size, f"Expected {fft_size} output samples, got {len(output)}"
    print("CLI run_fft_flow() basic test passed!")

if __name__ == "__main__":
    test_run_fft_flow()
    print("All tests passed!")