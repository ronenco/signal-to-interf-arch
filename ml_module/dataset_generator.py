# Generation of Datasets:
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# This is The library for the hardware simulation:

from general.helper_functions import generate_single_tone, generate_mixed_tones, generate_noise
import math
import numpy as np

def generate_dataset(num_samples, fft_size=64, noise_ratio=0.33):
    X = []
    y = []
    for _ in range(num_samples):
        if np.random.rand() < noise_ratio:
            # Generate noise sample
            signal = generate_noise(fft_size)
            label = 2  # Noise
        else:
            # Generate tone or tones
            signal, num_tones = generate_mixed_tones(fft_size)
            label = num_tones - 1  # 1-tone: label 0; 2-tone; label 1

        fft_result = np.fft.fft(signal)
        X.append(np.abs(fft_result))  # Magnitude spectrum
        y.append(label)

    X = np.array(X)
    y = np.array(y)
    return X, y


def main():
    # Example usage
    num_samples = 600  # 200 samples per class roughly
    fft_size = 64

    X, y = generate_dataset(num_samples, fft_size)

    print(f"Generated dataset shape: {X.shape}")
    print(f"Sample label distribution: {np.bincount(y)}")  # Quick label balance check

if __name__ == "__main__":
    main()