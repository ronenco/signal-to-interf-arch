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

    def read(self):
        """
        Read the value of the register.
        """
        # NOTE - This is a direct HW access to the register, therefore can't be accessed via CLI but only via the HW Module
        return self.value
    
    def write(self, value):
        """
        Write a value to the register.
        """
        # NOTE - This is a direct HW access to the register, therefore can't be accessed via CLI but only via the HW Module
        self.value = value

    def __repr__(self):
        return f"RegisterEntry(name={self.name}, address={self.address}, size={self.size}, access_type={self.access_type}, bind={self.bind})"

    def __str__(self):
        return f"RegisterEntry: {self.name} at address {self.address} with size {self.size} and access type {self.access_type}, bund {self.bind}"

## This is the base class for the register map:
# This class is used to read and write registers, and to bind modules to registers.
# It is a base class and should be inherited by other register maps.
class BaseRegisterMap:
    def __init__(self):
        self.register_map = {}
        self.bound_modules = {}

    def read_register(self, name):
        """
        Read a register value.
        """
        # Check if the register exists
        if name not in self.register_map:
            raise ValueError(f"Register {name} does not exist")
        # Check if the register is readable
        if self.register_map[name].access_type == "w":
            raise PermissionError(f"Register {name} is write-only")
        # Read the value from the register
        return self.register_map[name].value

    def write_register(self, name, value):
        """
        Write a value to a register.
        """
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

    def bind_module_to_register(self, module, register_name):
        """
        Bind a module to a register.
        """
        # Check if the register exists
        if register_name not in self.register_map:
            raise ValueError(f"Register {register_name} does not exist")
        # Bind the module to the register
        self.register_map[register_name].bind = module

    def update(self):
        for reg in self.register_map.values():
            if reg.bind and hasattr(reg.bind, "update"):
                reg.bind.update()

    def get_register(self, name):
        return self.register_map.get(name)

# This is the FftRegisterMap class:
class FFtRegisterMap(BaseRegisterMap):
    def __init__(self):
        """
        This is the FftRegisterMap class:
        """
        super().__init__() # Initialize the base class
        # Initialize the register map:
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

    def __repr__(self):
        return f"FFtRegisterMap(register_map={self.register_map})"
    
    def __str__(self):
        return f"FFtRegisterMap: {self.register_map}"

class ClassifierRegMap(BaseRegisterMap):
    def __init__(self):
        """
        This is the ClassifierRegMap class:
        """
        super().__init__()
        # Initialize the register map:
        # Register map
        self.register_map = {
            "CLASSIFY_TRIGGER":      RegisterEntry("CLASSIFY_TRIGGER", 0x20, 1, "rw"), 
            "CLASSIFY_RESULT":       RegisterEntry("CLASSIFY_RESULT", 0x21, 1, "r"),
            "CLASSIFY_DONE":         RegisterEntry("CLASSIFY_DONE", 0x22, 1, "r"), 
            "CLASSIFY_MODEL_SELECT": RegisterEntry("CLASSIFY_MODEL_SELECT", 0x23, 1, "rw"), # Model select
        }

    def __repr__(self):
        return f"ClassifierRegMap(register_map={self.register_map})"
    
    def __str__(self):
        return f"ClassifierRegMap: {self.register_map}"