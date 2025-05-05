import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware_sim.fft_block import FftBlock
from hardware_sim.buffer import Buffer
from hardware_sim.register_map import FFtRegisterMap, ClassifierRegMap
from interface.cli_controller import run_fft_flow
from general.helper_functions import create_fft_config, generate_single_tone, get_fft_size_code
from hardware_sim.classifier_block import ClassifierBlock

# This is a test for the ClassifierBlock class:
# To do this we first need to create a quick classifier and save it to a file (if it doesn't exist)
# So, first we check if the file exists, and if it doesn't, we create it
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"../ml_module/trained_rf_classifier.joblib"))

if not os.path.exists(model_path):
    print("Model file not found. Generating a new model...")
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    from ml_module.dataset_generator import generate_dataset
    import joblib


    num_samples = 600
    fft_size = 64

    X, y = generate_dataset(num_samples, fft_size)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # Train the RandomForestClassifier:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Print the classification report and accuracy
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Single Tone", "Two Tones", "Noise"]))
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")

    # Save the model
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")
else:
    print("Model file found. Proceeding with the test...")

# Now we create a test Classifier Block and test it:
# First we build the FFT block and the buffers:
fft_Input_buffer = Buffer(128, 64)
fft_Output_buffer = Buffer(128, 64)
hwFFT_block = FftBlock()
fft_block_reg_map = FFtRegisterMap()
fft_block_reg_map.bind_module_to_register(hwFFT_block, "FFT_START")
fft_block_reg_map.bind_module_to_register(hwFFT_block, "FFT_CONFIG")
fft_block_reg_map.bind_module_to_register(hwFFT_block, "FFT_DONE")
fftConfig = create_fft_config(
    fft_size_code=5,  # Corresponds to 64 FFT points
    zero_padding=0,
    normalization=1,
    phase_correction=0,
    phase_sign=0
)
fft_block_reg_map.write_register("FFT_CONFIG", fftConfig)
hwFFT_block.bind_input_output(fft_Input_buffer, fft_Output_buffer)

# Now we build the HW Classifier block and bind the bufferst to it:
hwClassifier = ClassifierBlock(model_path)
classifier_block_reg_map = ClassifierRegMap()
classifier_block_reg_map.bind_module_to_register(hwClassifier, "CLASSIFY_TRIGGER")
classifier_block_reg_map.bind_module_to_register(hwClassifier, "CLASSIFY_DONE")

hwClassifier.bind_input(fft_Output_buffer)
hwClassifier.bind_registers(classifier_block_reg_map.get_register("CLASSIFY_TRIGGER"), classifier_block_reg_map.get_register("CLASSIFY_RESULT"), 
                            classifier_block_reg_map.get_register("CLASSIFY_DONE"))

# Now we create a test signal and load it to the input buffer:
fft_size = hwFFT_block.getFFTSize()
signal = generate_single_tone(fft_size/2+1, fft_size)
fft_Input_buffer.writeBuffer(signal)
# Now we run the FFT block:
fft_block_reg_map.write_register("FFT_START", 1)
# Now we run the classifier block:
classifier_block_reg_map.write_register("CLASSIFY_TRIGGER", 1)
# Now we check the result:
result = classifier_block_reg_map.get_register("CLASSIFY_RESULT").read()
print(f"Classifier result: {result}")
# The result should be 0, since we have a single tone
# Now we check the done flag:
done = classifier_block_reg_map.get_register("CLASSIFY_DONE").read()
print(f"Classifier done flag: {done}")  
