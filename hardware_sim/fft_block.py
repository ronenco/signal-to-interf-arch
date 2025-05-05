# This is the fast fourier transform block:
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This is The library for the hardware simulation:
from hardware_sim.register_map import FFtRegisterMap
from hardware_sim.buffer import Buffer
from general.helper_functions import create_fft_config, generate_single_tone, get_fft_size
import math
import numpy as np

class FftBlock:
    def __init__(self):
        self.done = 0
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
        if not isinstance(config, int):
            raise ValueError("Configuration must be an integer")
        if config < 0 or config > 0xFFFFFFFF:
            raise ValueError("Configuration must be a 32-bit integer")
        self.config = config

        # Set up the FFT block with the given configuration
        self.parse_config(config)

    def bind_input_output(self, input_buffer, output_buffer):
        """
        Bind the input and output buffers to the FFT block.
        """
        if not isinstance(input_buffer, Buffer):
            raise ValueError("Input buffer must be a Buffer object")
        if not isinstance(output_buffer, Buffer):
            raise ValueError("Output buffer must be a Buffer object")
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer

    def load_input(self, input_data):
        """
        Load the input data into the FFT block.
        """
        self.input_data = input_data
        # Load the input data into the FFT block
        # This is a placeholder for actual hardware loading code
    
    def run(self):
        """
        Run the FFT block.
        """
        # Run the FFT block
        # This is a placeholder for actual hardware run code
        inputBuffer = self.getBufferSamples()
        if inputBuffer is None:
            return; # this is when padding behaviour is 1 and input data is too short
        # Check if the input buffer is the right size:
        if len(inputBuffer) != self.fft_size:
            raise ValueError("Input buffer was not the right size")
        
        # Perform Windowing:
        windowOutput = self.windowing(inputBuffer)

        # Perform FFT:
        fftOutput = self.fft(windowOutput)

        # Perform normalization:
        if self.normalization:
            fftOutput = self.normalize(fftOutput)

        # Perform phase shifting:
        if self.phaseDirection:
            fftOutput = self.phaseShift(fftOutput, self.phaseValue)
        else:
            fftOutput = self.phaseShift(fftOutput, -self.phaseValue)

        # Save to the output buffer:
        if self.output_buffer is not None:
            self.output_buffer.writeBuffer(fftOutput)
        else:
            self.output_data = fftOutput

        # Set the done flag
        self.done = 1

    
    def get_output(self):
        """
        Get the output data from the FFT block.
        """
        if self.output_buffer:
            return self.output_buffer.getBuffer()
        else:
            return self.output_data


    def handle_FFT_START(self, value):
        """
        Handle the FFT start register.
        """
        if value == 1:
            self.run()

    def handle_FFT_CONFIG(self, value):
        """
        Handle the FFT configuration register.
        """
        self.configure(value)

    def update(self, name, value):
        """
        Update the FFT block with the given register name and value.
        """
        print(f"Fallback update for {name} = {value}")


    def parse_config(self, config):
        """
        Parse the configuration for the FFT block.
        """
        # Parse the configuration for the FFT block
        # The first 4 bits are the fft size index:
        fftSizeIndex = config & 0x0F
        print("FFT size index: ", fftSizeIndex)
        if fftSizeIndex > 11:
            raise ValueError("Invalid FFT size") #TODO: add other options (only zero for input, noise, etc)
        # Set the fft size
        self.fft_size = get_fft_size(fftSizeIndex)
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

    def getBufferSamples(self):
        """
        Get the buffer samples for the FFT block, depending on padding behaviour.
        """
        # Padding behaviour:
        # 0 : No zero padding, error if input is too short
        # 1 : No zero padding, do nothing if input is too short
        # 2 : Zero padding, padd from the beginning if input is too short
        # 3 : Zero padding, padd from the end if input is too short
        
        # But first, we get the input data:
        # if we have a buffer, we need to get the data from it
        # if we don't have a buffer, we need to get the data from the input data
        if self.input_buffer is None:
            bufferIn = self.input_data
        else:
            bufferIn = self.input_buffer.getBuffer()
        
        if self.paddingBehaviour == 0:
            if len(bufferIn) < self.fft_size:
                raise ValueError("Input data is too short, was expecting " + str(self.fft_size) + " samples, got " + str(len(bufferIn)) + " samples")

        elif self.paddingBehaviour == 1:
            if len(bufferIn) < self.fft_size:
                return # this is when padding behaviour is 1 and input data is too short
        elif self.paddingBehaviour == 2:
            if len(bufferIn) < self.fft_size:
                # we need to pad the input data with zeros
                bufferIn = [0] * (self.fft_size - len(bufferIn)) + bufferIn

        elif self.paddingBehaviour == 3:
            if len(bufferIn) < self.fft_size:
                # we need to pad the input data with zeros
                bufferIn = bufferIn + [0] * (self.fft_size - len(bufferIn))

        # Shared between all cases:
        # we only need the first fft_size values
        if self.input_buffer is not None:
            # if we have a buffer, we need to clear it
            # and write the new data to it
            self.input_buffer.clear()
            self.input_buffer.writeBuffer(bufferIn[self.fft_size:])
        # clean whatever samples are in bufferIn:
        bufferIn = bufferIn[:self.fft_size]
        return bufferIn

    def windowing(self, inputBuffer):
        """
        Perform windowing on the input buffer.
        """
        # Perform windowing on the input buffer
        # This is a placeholder for actual hardware windowing code

        # For now, we just return the input buffer (which is a rectangle)
        return inputBuffer
    
    def fft(self, inputBuffer):
        """
        Perform FFT on the input buffer.
        """
        # Perform FFT on the input buffer
        # This is a placeholder for actual hardware FFT code
        fftOut = np.fft.fft(inputBuffer)
        # For now, we just return the input buffer (which is a rectangle)
        return fftOut
    
    def normalize(self, inputBuffer):
        """
        Perform normalization on the input buffer.
        """
        # Perform normalization on the input buffer
        # This is a placeholder for actual hardware normalization code

        # For now, we just return the input buffer (which is a rectangle)
        return inputBuffer/math.sqrt(self.fft_size)

    def phaseShift(self, inputBuffer, phaseValue):
        """
        Perform phase shifting on the input buffer.
        """
        # Perform phase shifting on the input buffer
        # This is a placeholder for actual hardware phase shifting code

        # For now, we just return the input buffer (which is a rectangle)
        return inputBuffer * np.exp(1j * phaseValue)
    
    def getFFTSize(self):
        """
        Get the FFT size.
        """
        return self.fft_size
    
    def __repr__(self):
        return f"FFTBlock(fft_size={self.fft_size}, paddingBehaviour={self.paddingBehaviour}, phaseValue={self.phaseValue}, phaseDirection={self.phaseDirection}, normalization={self.normalization}, reserved={self.reserved})"
    def __str__(self):
        return f"FFTBlock: fft_size={self.fft_size}, paddingBehaviour={self.paddingBehaviour}, phaseValue={self.phaseValue}, phaseDirection={self.phaseDirection}, normalization={self.normalization}, reserved={self.reserved}"
    def __len__(self):
        if self.input_buffer is not None:
            return len(self.input_buffer)
        else:
            return 0