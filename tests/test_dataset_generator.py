# This script tests the dataset generation function from the ml_module.
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml_module.dataset_generator import generate_dataset

def test_generate_dataset():
    num_samples = 600
    fft_size = 64

    X, y = generate_dataset(num_samples, fft_size)

    # Shape tests
    assert X.shape == (num_samples, fft_size), f"Expected X shape {(num_samples, fft_size)}, got {X.shape}"
    assert y.shape == (num_samples,), f"Expected y shape {(num_samples,)}, got {y.shape}"

    # Label tests
    unique_labels = set(np.unique(y))
    assert unique_labels.issubset({0, 1, 2}), f"Unexpected labels found: {unique_labels}"

    # No NaNs or infs
    assert np.isfinite(X).all(), "Found NaNs or infinities in X"

    # Label distribution (optional loose check)
    label_counts = np.bincount(y)
    print(f"Label distribution: {label_counts}")

    assert len(label_counts) == 3, f"Expected 3 classes, found {len(label_counts)}"

    print("Dataset generation test passed!")

if __name__ == "__main__":
    test_generate_dataset()
    print("All tests passed.")
