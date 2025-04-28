# This is the library for the helper functions in the signal to interfirence repository:
#  

import numpy as np

def get_fft_size_code(fft_size):
    """
    Get the FFT size code based on the FFT size.
    """
    if fft_size == 64:
        return 0
    elif fft_size == 128:
        return 1
    elif fft_size == 256:
        return 2
    elif fft_size == 512:
        return 3
    elif fft_size == 1024:
        return 4
    elif fft_size == 2048:
        return 5
    elif fft_size == 4096:
        return 6
    elif fft_size == 8192:
        return 7
    else:
        raise ValueError("Invalid FFT size. Supported sizes are: 64, 128, 256, 512, 1024, 2048, 4096, and 8192.")

def get_fft_size(fft_size_code):
    """
    Get the FFT size based on the FFT size code.
    """
    fft_size_lookup = {0:2, 1:4, 2:8, 3:16, 4:32, 5:64, 6:128, 7:256, 8:512, 9:1024, 10:2048, 11:4096}
    return fft_size_lookup.get(fft_size_code, None) # Returns None if code is invalid

def create_fft_config(fft_size_code, zero_padding, normalization, phase_correction, phase_sign):
    """
    Helper to create a 32-bit config word for the FFT block.
    """
    config = 0
    config |= (fft_size_code & 0xF)          # 4 bits for fft_size_code
    config |= (zero_padding & 0x03) << 4       # 2 bits for zero padding behavior
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

def generate_mixed_tones(fft_size, possible_tones=2):
    """
    Generate a mixed-tone signal with a random number of tones.
    """
    # Randomly choose the number of tones
    num_tones = np.random.choice([tones for tones in range(1,possible_tones+1)])
    total_signal = np.zeros(fft_size, dtype=complex)
    used_bins = set()

    for _ in range(num_tones):
        available_bins = [b for b in range(1, fft_size//2) if b not in used_bins]
        if not available_bins:
            break  # No available bins left
        random_bin = np.random.choice(available_bins)
        used_bins.add(random_bin)
        
        tone = generate_single_tone(random_bin, fft_size)  # reuse your helper function!
        total_signal += tone

    return total_signal, num_tones

def generate_noise(fft_size):
    """
    Generate complex Gaussian noise.
    """
    # Create complex Gaussian noise (mean=0, variance=1)
    noise_real = np.random.randn(fft_size)
    noise_imag = np.random.randn(fft_size)
    noise = (noise_real + 1j * noise_imag) / np.sqrt(2)  # Normalize for unit average power
    return noise
