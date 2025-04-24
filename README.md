# Signal-to-Inference Architecture Simulation

This project simulates a full signal-to-inference pipeline for an AI inference system-on-chip (SoC). It models a real-time system that integrates traditional DSP blocks (like FFT) with neural network inference, all controlled via a simulated register interface.

> ⚙️ Bridging signal processing with machine learning in a hardware-aware architecture.

## 🎯 Project Goals

- Demonstrate **system-level thinking** in AI platform design
- Integrate **signal preprocessing** with **PyTorch inference**
- Simulate **hardware/software interface** via register control
- Provide a modular and testable platform for AI SoC experimentation

## 📐 System Architecture

                +---------------------+
                |   I/Q Signal Input   |
                +----------+----------+
                           |
                           v
                    +-------------+
                    |  FFT Engine | <───[Controlled via Register File]
                    +------+------+ 
                           |
                           v
              +-------------------------+
              | Feature Extractor (Opt) |  ← e.g., magnitude, energy
              +------------+------------+
                           |
                           v
                +----------------------+
                |  PyTorch AI Classifier|
                +-----------+----------+
                            |
                            v
             +----------------------------+
             | Result Output Register File |
             +----------------------------+

## 🔄 Control Interface (Software Simulation)

                +-------------------------+
                |     Register Map       |
                |-------------------------|
                | 0x00: FFT Size         |
                | 0x04: Window Type      |
                | 0x08: Enable Inference |
                | 0x0C: Inference Result |
                +-----------+-------------+
                            ^
                            |
                      +-----+-----+
                      | CLI Tool  |
                      +-----------+


## Folder structure:

```
signal-to-inference-arch/
├── model/
│   └── rf_classifier.py           # Tiny PyTorch model (starter)
├── hardware_sim/
│   ├── fft_block.py               # Simulated FFT module using numpy
│   ├── register_map.py            # Simple class for memory-mapped register simulation
│   └── system_runner.py           # Orchestrates the full pipeline
├── interface/
│   └── cli_controller.py          # CLI to write/read registers, trigger inference
├── tests/
│   └── test_pipeline.py           # Basic pipeline test case
├── README.md                      # Overview + diagram + usage
└── requirements.txt               # Dependencies: numpy, torch, etc.
```
## 🔧 Getting Started

### Prerequisites
- Python 3.8+
- `pip install -r requirements.txt`

### Run the CLI:

``` bash

python interface/cli_controller.py

# Set FFT size to 128
set_reg fft_size 128

# Enable model inference
set_reg model_enable 1

# Load input samples (file or mock)
run_pipeline input_samples.npy

```


👨‍💻 Author
- Ronen Cohen
- System Architect & Algorithm Engineer
- LinkedIn: Contact Me
- GitHub: https://github.com/ronenco/

