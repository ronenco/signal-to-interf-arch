import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import joblib
import numpy as np
from hardware_sim.register_map import ClassifierRegMap
from hardware_sim.buffer import Buffer

class ClassifierBlock:
    def __init__(self, model_path="ml_module/trained_rf_classifier.joblib"):
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

    def update(self):
        if self.triggered and self.input_buffer is not None:
            signal = self.input_buffer.getBuffer()

            if signal is None or len(signal) == 0:
                print("ClassifierBlock: Input buffer is empty.")
                return

            fft_result = np.fft.fft(signal)
            features = np.abs(fft_result).reshape(1, -1)
            label = self.model.predict(features)[0]

            if self.output_registers.get('result'):
                self.output_registers['result']['value'] = label
            if self.output_registers.get('done'):
                self.output_registers['done']['value'] = 1

            self.triggered = False

    def __str__(self):
        return f"<ClassifierBlock (latency={self.latency_cycles} cycles)>"


