import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This is The library for the hardware simulation:
from hardware_sim.buffer import Buffer
import numpy as np
import math


def test_buffer_basic():
    buffer = Buffer(max_size=10, bufferFullSize=5)
    # Test writing to the buffer
    data = [1, 2, 3, 4, 5]
    buffer.writeBuffer(data)
    # Test buffer size
    assert len(buffer) == len(data)
    # Test buffer full
    data_out = buffer.getBuffer()
    assert np.array_equal(data_out, np.array(data, dtype=complex))

def test_buffer_full_and_empty():
    buffer = Buffer(max_size=10, bufferFullSize=5)
    # Test empty buffer
    assert buffer.isEmpty() == True
    # Test writing to the buffer
    data = [1, 2, 3, 4, 5]
    buffer.writeBuffer(data)
    # Test buffer full
    assert buffer.isFull() == True
    # Test emptying the buffer
    buffer.clear()
    assert buffer.isEmpty() == True

def test_buffer_clear():
    buffer = Buffer(max_size=10, bufferFullSize=5)
    # Test writing to the buffer
    data = [1, 2, 3, 4, 5, 6 ,7, 8, 9, 10]
    buffer.writeBuffer(data)
    # Test clearing the buffer
    buffer.clear()
    assert buffer.isEmpty() == True

def test_buffer_errors():
    buffer = Buffer(max_size=10, bufferFullSize=5)
    # Test writing invalid data type
    try:
        buffer.writeBuffer("invalid data")
    except TypeError as e:
        assert str(e) == "Buffer data must be a list or numpy array"
    
    # Test writing data exceeding max size
    try:
        buffer.writeBuffer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    except ValueError as e:
        assert str(e) == "Data exceeds buffer max size 10"

    # Test setting bufferFullSize greater than max_size
    try:
        Buffer(max_size=5, bufferFullSize=10)
    except ValueError as e:
        assert str(e) == "Buffer max size cannot exceed buffer full size"
    
if __name__ == "__main__":
    test_buffer_basic()
    test_buffer_full_and_empty()
    test_buffer_clear()
    test_buffer_errors()
    print("All Buffer Tests Passed!")