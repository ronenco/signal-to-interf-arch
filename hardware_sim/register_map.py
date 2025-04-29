# Register map
# This file contains the register map for the hardware simulation.
# The register map is a dictionary that maps register names to their addresses and sizes.
# To access the register map use the registerEntry class:

class RegisterEntry:
    def __init__(self, name, address, size, access_type="rw", bind = None):
        # Check inputs:
        if access_type not in ["rw", "r", "w"]:
            raise ValueError("Access type must be 'rw', 'r' or 'w'")
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not isinstance(address, int):
            raise ValueError("Address must be an integer")
        if not isinstance(size, int):
            raise ValueError("Size must be an integer")
        # Enter the register entry:
        self.name = name
        self.address = address
        self.size = size
        self.access_type = access_type
        self.bind = bind
        self.value = 0 # Default value

    def __repr__(self):
        return f"RegisterEntry(name={self.name}, address={self.address}, size={self.size}, access_type={self.access_type}, bind={self.bind})"

    def __str__(self):
        return f"RegisterEntry: {self.name} at address {self.address} with size {self.size} and access type {self.access_type}, bund {self.bind}"

# This is the FftRegisterMap class:
class FFtRegisterMap:
    def __init__(self):
        # Register map
        self.register_map = {
            "FFT_START":    RegisterEntry("FFT_START", 0x00, 1, "rw"),   # Start the FFT
            "FFT_DONE":     RegisterEntry("FFT_DONE", 0x01, 1, "r"),     # Done signal
            "FFT_DATA_IN":  RegisterEntry("FFT_DATA_IN", 0x02, 4, "rw"), # Input data
            "FFT_DATA_OUT": RegisterEntry("FFT_DATA_OUT", 0x06, 4, "r"), # Output data
            "FFT_CONFIG":   RegisterEntry("FFT_CONFIG", 0x0A, 4, "rw"),  # Configuration register
            "FFT_STATUS":   RegisterEntry("FFT_STATUS", 0x0E, 1, "r"),   # Status register
            "WINDOW_SIZE":  RegisterEntry("WINDOW_SIZE", 0x0F, 1, "rw"), # Window size
            "WINDOW_TYPE":  RegisterEntry("WINDOW_TYPE", 0x10, 1, "rw"), # Window type
        }

    def write_register(self, name, value):
        # Check if the register exists
        if name not in self.register_map:
            raise ValueError(f"Register {name} does not exist")
        # Check if the value is within the range of the register size
        reg = self.register_map[name]
        if value < 0 or value >= 2 ** (reg.size * 8):
            raise ValueError(f"Value {value} is out of range for register {name}")
        # Write the value to the register
        if reg.access_type == "r":
            raise PermissionError(f"Register {name} is read-only")
        
        reg.value = value
        
        if reg.bind is not None:
            if hasattr(reg.bind, f"handle_{name}"):
                handler = getattr(reg.bind, f"handle_{name}")
                handler(value)
            else:
                reg.bind.update(name, value)
    
    def read_register(self, name):
        # Check if the register exists
        if name not in self.register_map:
            raise ValueError(f"Register {name} does not exist")
        # Read the value from the register
        return self.register_map[name].value
    
    def bind_module_to_register(self, module, register_name):
        # Check if the register exists
        if register_name not in self.register_map:
            raise ValueError(f"Register {register_name} does not exist")
        # Bind the module to the register
        self.register_map[register_name].bind = module
    
    def __repr__(self):
        return f"FFtRegisterMap(register_map={self.register_map})"
    
    def __str__(self):
        return f"FFtRegisterMap: {self.register_map}"

def ClassifierRegMap():
    """
    This function returns the register map for the Classifier block.
    """
    self.register_map = {
        "CLASSIFY_TRIGGER": RegisterEntry("CLASSIFY_TRIGGER", 0x20, 1, "rw"), 
        "CLASSIFY_RESULT":  RegisterEntry("CLASSIFY_RESULT", 0x21, 1, "r"),
        "CLASSIFY_DONE":    RegisterEntry("CLASSIFY_DONE", 0x22, 1, "r"),
    }