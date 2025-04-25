# This is the fast fourier transform block:
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This is The library for the hardware simulation:
from hardware_sim.register_map import FFtRegisterMap
from hardware_sim.buffer import Buffer
import math
class FFTBlock:
    def __init__(self):
        self.fft_size = 0
        self.paddingBehaviour = 0
        self.phaseValue = 0
        self.phaseDirection = 0
        self.normalization = 0
        self.reserved = 0
        self.config = None
        self.output_data = None
        self.input_data = None
        self.input_buffer = None
        self.output_buffer = None

    def configure(self, config):
        """
        Configure the FFT block with the given configuration.
        """
        self.config = config
        # Set up the FFT block with the given configuration
        # This is a placeholder for actual hardware configuration code
        print(f"Configuring FFT block with config: {config}")
    
    def load_input(self, input_data):
        """
        Load the input data into the FFT block.
        """
        self.input_data = input_data
        # Load the input data into the FFT block
        # This is a placeholder for actual hardware loading code
        print(f"Loading input data: {input_data}")
    
    def run(self):
        """
        Run the FFT block.
        """
        # Run the FFT block
        # This is a placeholder for actual hardware running code
        print("Running FFT block...")
    
    def get_output(self):
        if self.output_buffer:
            return self.output_buffer.getBuffer()
        else:
            return self.output_data

    def update(self, valued):
        """
        Update the FFT block with the given value.
        """
        # Update the FFT block with the given value
        # This is a placeholder for actual hardware update code
        print(f"Updating FFT block with value: {value}")
        
    def parse_config(self, config):
        """
        Parse the configuration for the FFT block.
        """
        # Parse the configuration for the FFT block
        # The first 4 bits are the fft size index:
        fft_table = {
            0: 2,
            1: 4,
            2: 8,
            3: 16,
            4: 32,
            5: 64,
            6: 128,
            7: 256,
            8: 512,
            9: 1024,
            10: 2048,
            11: 4096,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
        }
        fftSizeIndex = config & 0x0F
        if fftSizeIndex > 11:
            raise ValueError("Invalid FFT size") #TODO: add other options (only zero for input, noise, etc)
        # Set the fft size
        self.fft_size = fft_table[fftSizeIndex]
        # The next 2 bits are the padding information:
        paddingBehaviour = (config >> 4) & 0x03
        self.paddingBehaviour = paddingBehaviour
        # The next 11 bits are the phase value:
        phaseValue = (config >> 6) & 0x7FF
        self.phaseValue = phaseValue/ (2**11) * math.pi
        self.phaseDirection = 1 - 2*((config >> 17) & 0x01) #if 0, phase is positive, if 1, phase is negative
        # The next bit is for normalization:
        self.normalization = (config >> 18) & 0x01
        # The rest of the bits are reserved:
        self.reserved = (config >> 19)
        # Check if the configuration is valid
        if self.fft_size == 0:
            raise ValueError("Invalid FFT size")
        if self.paddingBehaviour > 3:
            raise ValueError("Invalid paddingBehaviour")
        if self.phaseValue > 2*math.pi:
            raise ValueError("Invalid phase value")
        if self.phaseDirection > 1:
            raise ValueError("Invalid phase direction")
        if self.normalization > 1:
            raise ValueError("Invalid normalization value")
        if self.reserved > 0:
            raise ValueError("Invalid reserved value")
        # Save the configuration
        self.config = config