# Signal-to-Inference System — CLI Controller
This folder contains the Command Line Interface (CLI) controller for interacting with the Signal-to-Inference platform simulation.

The CLI allows manual read/write access to hardware-mapped registers, runs predefined flows (like FFT triggering), and inspects system state — mimicking a real embedded system control environment.

## Available CLI Commands:

| Command                         | Arguments                      | Description                                 |
|---------------------------------|--------------------------------|---------------------------------------------|
| set_reg <register_name> <value> | Register name and value        | Set a specific register (hex/decimal).      |
| get_reg <register_name>         | Register name                  | Read and display register value.            |
| dump_reg                        | None                           | Print all available registers.              |
| run_fft                         | None                           | Load default signal, set config, start FFT. |
| exit                            | None                           | Exit the CLI cleanly.                       |


## System Setup Notes:

Before starting the CLI:

Buffers (input and output) must be bound to the FFT block.

FFT block must be bound to critical registers like FFT_START and FFT_CONFIG.

Example Initialization Flow:

```python

from hardware_sim.fft_block import FftBlock
from hardware_sim.buffer import Buffer
from hardware_sim.register_map import FFtRegisterMap
from interface.cli_controller import cli_controller

# Instantiate system components
fft_block = FftBlock()
input_buffer = Buffer(max_size=4096)
output_buffer = Buffer(max_size=4096)

# Bind input/output buffers
fft_block.bind_input_output(input_buffer, output_buffer)

# Create register map and bind modules
register_map = FFtRegisterMap()
register_map.bind_module_to_register(fft_block, "FFT_START")
register_map.bind_module_to_register(fft_block, "FFT_CONFIG")

# Launch CLI
cli_controller(register_map, fft_block)

```

## Folder Overview

| File                  | Purpose                                                               |
|-----------------------|-----------------------------------------------------------------------|
| `cli_controller.py`   | Main CLI loop and command parsing logic for the platform simulation.  |

## Future Extensions

- `help` command listing all available commands.
- Load custom signals (random, multiple tones).
- Advanced control: phase correction, windowing selection.
- Error injection testing.

Contributions and improvements are welcome as the system grows!

** Note on Enviorment: **
If using the CLI inside different environments (e.g., SSH, Jupyter Notebooks), input/output behaviors may vary slightly.