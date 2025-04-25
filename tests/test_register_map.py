# This is a test file for the register map of the FFT block.
#
# This file contains the test cases for the register map of the FFT block.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This is The library for the hardware simulation:
from hardware_sim.register_map import FFtRegisterMap


def test_register_read_write():
    """
    Test the read and write functions of the register map.
    """
    print("Testing register read and write functions...")

    # Create a register map
    fft_register = FFtRegisterMap()

    # Write to a register
    fft_register.write_register("FFT_START", 1)
    assert fft_register.register_map["FFT_START"].value == 1

    # Read from a register
    value = fft_register.read_register("FFT_START")
    assert value == 1

    # Try writing to a read-only register (should fail)
    try:
        fft_register.write_register("FFT_DONE", 1)
    except PermissionError as e:
        print(f"Caught expected error: {e}")

    # Try writing an out-of-range value (should fail)
    try:
        fft_register.write_register("FFT_DATA_IN", 2**32)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Try reading a non-existent register
    try:
        fft_register.read_register("NON_EXISTENT")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Try writing to a non-existent register
    try:
        fft_register.write_register("NON_EXISTENT", 1)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    print("All tests passed!")

if __name__ == "__main__":
    test_register_read_write()
    print("Test completed.")