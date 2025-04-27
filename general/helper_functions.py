# This is the library for the helper functions in the signal to interfirence repository:
#  
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
