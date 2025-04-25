# This file is part of the hardware_sim package.
# It is a simulation of a hardware buffer
import numpy as np

class Buffer:
    def __init__(self, max_size=None, bufferFullSize=None):
        self.buffer = None
        self.max_size = max_size
        self.bufferFullSize = bufferFullSize if bufferFullSize is not None else max_size
        if self.max_size is not None and self.bufferFullSize is not None:
            if self.max_size < self.bufferFullSize:
                raise ValueError("Buffer max size cannot exceed buffer full size")

    def writeBuffer(self, data):
        if isinstance(data, list) or isinstance(data, np.ndarray):
            if self.max_size and len(data) > self.max_size:
                raise ValueError(f"Data exceeds buffer max size {self.max_size}")
            self.buffer = np.array(data, dtype=complex)
        else:
            raise TypeError("Buffer data must be a list or numpy array")

    def getBuffer(self):
        return self.buffer

    def clear(self):
        self.buffer = None

    def isFull(self):
        if self.buffer is not None:
            return len(self.buffer) >= self.bufferFullSize
        else:
            return False
    
    def isEmpty(self):
        if self.buffer is not None:
            return len(self.buffer) == 0
        else:
            return True

    def __len__(self):
        if self.buffer is not None:
            return len(self.buffer)
        else:
            return 0

    