# tests/test_pipeline.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware_sim.fft_block import FftBlock
from hardware_sim.register_map import FFtRegisterMap
from hardware_sim.buffer import Buffer
import numpy as np
import math

def create_fft_config(fft_size_code, zero_padding, normalization, phase_correction, phase_sign):
    """
    Helper to create a 32-bit config word for the FFT block.
    """
    config = 0
    config |= (fft_size_code & 0xF)          # 4 bits for fft_size_code
    config |= (zero_padding & 0x3) << 4       # 2 bits for zero padding behavior
    config |= (phase_correction & 0x7FF) << 6 # 11 bits for phase correction value
    config |= (phase_sign & 0x1) << 17        # 1 bit for phase sign
    config |= (normalization & 0x1) << 18     # 1 bit for normalization enable
    return config

def generate_single_tone(frequency_bin, fft_size):
    """
    Generate a single-tone complex sinusoidal signal.
    """
    n = np.arange(fft_size)
    tone = np.exp(1j * 2 * np.pi * frequency_bin * n / fft_size)
    return tone

def test_full_system_flow():
    """
    Full system integration test: RegisterMap + FFTBlock + Buffers working together.
    """
    # 1. Initialize system components
    reg_map = FFtRegisterMap()
    fft_block = FftBlock()
    input_buffer = Buffer(4096, 4096)  # Current buffer supports up to 4096 samples
    output_buffer = Buffer(4096, 4096)  # Current buffer supports up to 4096 samples

    # 2. Bind FFTBlock to FFT_START register
    reg_map.bind_module_to_register(fft_block, "FFT_START")
    # This assumes FFTBlock has a method to bind to the register map

    # 3. Bind input and output buffers to FFTBlock
    fft_block.bind_input_output(input_buffer, output_buffer)



    # 4. Load input samples
    fft_size_code = 5  # Index 5 → FFT size 64
    fft_size_lookup = {0:2, 1:4, 2:8, 3:16, 4:32, 5:64, 6:128, 7:256, 8:512, 9:1024, 10:2048, 11:4096}
    fft_size = fft_size_lookup[fft_size_code]
    input_signal = generate_single_tone(frequency_bin=5, fft_size=fft_size)
    input_buffer.writeBuffer(input_signal)

    # 5. Write configuration to registers
    config = create_fft_config(
        fft_size_code=fft_size_code,
        zero_padding=0,
        normalization=1,
        phase_correction=0,
        phase_sign=0
    )
    reg_map.bind_module_to_register(fft_block, "FFT_CONFIG")
    reg_map.write_register("FFT_CONFIG", config)

    # 6. Trigger FFT by writing 1 to FFT_START
    reg_map.write_register("FFT_START", 1)

    # 7. Validate output
    output = output_buffer.getBuffer()
    assert output is not None, "Output buffer is empty after FFT run!"
    assert len(output) == fft_size, f"FFT output size mismatch: expected {fft_size}, got {len(output)}"

    print("FFT Output Magnitudes:")
    print(np.abs(output))

    # 8. (Optional) Check FFT_DONE flag (if your FFTBlock sets it)
    # Example: assert reg_map.read_register("FFT_DONE") == 1

if __name__ == "__main__":
    test_full_system_flow()
    print("Full system flow test passed!")