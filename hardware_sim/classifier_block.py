import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import joblib
import numpy as np
from hardware_sim.register_map import ClassifierRegMap
from hardware_sim.buffer import Buffer

class ClassifierBlock:
    def __init__(self, model_path="ml_module/trained_rf_classifier.joblib"):
        self.model_path = model_path
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not model_path.endswith('.joblib'):
            raise ValueError("Model file must be a .joblib file")
        if not os.path.isfile(model_path):
            raise ValueError("Model path must be a file")
        if not os.access(model_path, os.R_OK):
            raise PermissionError(f"Model file is not readable: {model_path}")
        # Load the trained model
        self.model = joblib.load(model_path)
        self.input_buffer = None
        self.output_registers = {}
        self.latency_cycles = 0
        self.triggered = False

    def bind_input(self, buffer):
        """
        Bind the input buffer to the classifier block.
        """
        self.input_buffer = buffer

    def bind_registers(self, classify_trigger_reg, classify_result_reg, classify_done_reg=None):
        """
        Bind the registers to the classifier block.
        """
        self.output_registers['trigger'] = classify_trigger_reg
        self.output_registers['result'] = classify_result_reg
        self.output_registers['done'] = classify_done_reg

    def handle_CLASSIFY_TRIGGER(self, value):
        if value == 1:
            self.triggered = True
            self.run()
        self.triggered = False
    
    def handle_CLASSIFY_MODEL_SELECT(self, value):
        model_paths = {
            0: "ml_module/model_rf_classifier.joblib",
            1: "ml_module/model_rf_snr_augmented.joblib",
            2: "ml_module/model_rf_fft128.joblib",
            3: "ml_module/model_rf_fft512.joblib"
        }
        selected_path = model_paths.get(value)
        if selected_path:
            if not os.path.exists(selected_path):
                raise FileNotFoundError(f"Model file not found: {selected_path}")
            if not os.path.isfile(selected_path):
                raise ValueError("Model path must be a file")
            if not os.access(selected_path, os.R_OK):
                raise PermissionError(f"Model file is not readable: {selected_path}")
            self.model = joblib.load(selected_path)
            if self.output_registers.get('done'):
                self.output_registers['done'].write(0)
        else:
            raise ValueError(f"Invalid model selection {value}. Valid options are: {list(model_paths.keys())}")




    def run(self):
        if self.triggered and self.input_buffer is not None:
            fft_result = self.input_buffer.getBuffer()

            if fft_result is None or len(fft_result) == 0:
                print("ClassifierBlock: Input buffer is empty.")
                return

            features = np.abs(fft_result).reshape(1, -1)
            label = self.model.predict(features)[0]

            # Write to the registers if initiated using the register's object write command:
            if self.output_registers.get('result'):
                self.output_registers['result'].write(label) # this is direct access to register so it bypasses read only condition
            if self.output_registers.get('done'):
                self.output_registers['done'].write(1) #this is direct access to register so it bypasses read only condition

            self.triggered = False

    def update(self):
        if self.triggered:
            self.run()


    def __str__(self):
        return f"<ClassifierBlock (latency={self.latency_cycles} cycles, triggered={self.triggered}, model_path={self.model_path})>"

    def __repr__(self):
        return self.__str__()
