# CLI (Command-Line Interface) to write/read registers, trigger inference
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This is The library for the hardware simulation:
from hardware_sim.register_map import FFtRegisterMap
from hardware_sim.fft_block import FftBlock
from hardware_sim.buffer import Buffer
from general.helper_functions import create_fft_config, generate_single_tone, get_fft_size
import math
import numpy as np

def cli_controller(register_map, fft_block):
    """
    Command-line interface to control the FFT block and register map.
    """
    while True:
        print("\n--- FFT Block Control ---")
        print("1. Set Register - set_reg")
        print("2. Read Register - get_reg")
        print("3. View All Registers - dump_reg")
        print("4. Run FFT Flow - run_fft")
        print("5. Exit - exit")
        
        choice = input("Enter your choice: ")
        choice = choice.split(" ")
        if choice[0] == "set_reg":
            reg_name = choice[1]
            value = int(choice[2])
            try:
                register_map.write_register(reg_name, value)
                print(f"Written {value} to {reg_name}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice[0] == "get_reg":
            reg_name = choice[1]
            try:
                value = register_map.read_register(reg_name)
                print(f"Value of {reg_name}: {value}")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice[0] == "dump_reg":
            print("Register Map:")
            for reg_name, reg in register_map.register_map.items():
                print(f"{reg_name}: {reg.value}")
        elif choice[0] == "run_fft":
            run_fft_flow(register_map, fft_block)
            # Load input data into the FFT block
                    
        elif choice[0] == 'exit':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

def run_fft_flow(register_map, fft_block):
    print("Running FFT flow...")

    # 1. Check if FFT_CONFIG is already set
    try:
        config_value = register_map.read_register("FFT_CONFIG")
    except Exception:
        config_value = None

    if config_value is None or config_value == 0:
        print("No FFT_CONFIG set. Applying default configuration...")
        config_value = create_fft_config(
            fft_size_code=5,   # Default 64-point FFT
            zero_padding=0,
            normalization=1,
            phase_correction=0,
            phase_sign=0
        )
        register_map.write_register("FFT_CONFIG", config_value)
    else:
        print(f"Using existing FFT_CONFIG: 0x{config_value:08X}")

    # 2. Parse fft_size_code from config
    fft_size_code = config_value & 0xF
    fft_size = get_fft_size(fft_size_code)
    # default to 64 if unknown
    if fft_size is None:
        print("Unknown FFT size code. Defaulting to 64.")
        fft_size = 64

    # 3. Generate a signal
    input_signal = generate_single_tone(frequency_bin=5, fft_size=fft_size)

    # 4. Write input to buffer
    if fft_block.input_buffer:
        fft_block.input_buffer.writeBuffer(input_signal)
    else:
        print("Warning: No input buffer bound to FFTBlock.")

    # 5. Start FFT
    register_map.write_register("FFT_START", 1)
    print("FFT triggered.")

