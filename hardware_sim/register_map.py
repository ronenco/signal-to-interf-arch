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
        if not isinstance(bind, str) and bind not in [None, "None"]:
            raise ValueError("Bind is not yet set to be other than None")
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
            "FFT_CONFIG":   RegisterEntry("FFT_CONFIG", 0x0A, 10, "rw"), # Configuration register
            "FFT_STATUS":   RegisterEntry("FFT_STATUS", 0x14, 1, "r"),   # Status register
        }

    def write_register(self, name, value):
        # Check if the register exists
        if name not in self.register_map:
            raise ValueError(f"Register {name} does not exist")
        # Check if the value is within the range of the register size
        if value < 0 or value >= 2 ** (self.register_map[name].size * 8):
            raise ValueError(f"Value {value} is out of range for register {name}")
        # Write the value to the register
        if self.register_map[name].access_type == "r":
            raise PermissionError(f"Register {name} is read-only")
        
        self.register_map[name].value = value
        
        if self.register_map[name].bind is not None:
            # If the register is bound to another register, update the bound register
            self.register_map[self.register_map[name]["bind"]].value = value
    
    def read_register(self, name):
        # Check if the register exists
        if name not in self.register_map:
            raise ValueError(f"Register {name} does not exist")
        # Read the value from the register
        return self.register_map[name].value
    
    def __repr__(self):
        return f"FFtRegisterMap(register_map={self.register_map})"
    
