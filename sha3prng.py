import hashlib
import secrets
import copy

class prng:
    def __init__(self, seed = None):
        self._key = b'\x00' * 32
        if seed is None:
            self.__key = secrets.token_bytes(32)
        elif isinstance(seed, bytes):
            if len(seed) != 32:
                raise ValueError("Bytes object must be 256-bits (32 bytes) long for the seed.")
            self.__key = seed
        elif isinstance(seed, int):
            if seed > (2**256 - 1) or seed < 0:
                raise ValueError("Seed must be a non-negative integer not greater than 2^256-1.")
            self.__key = int(seed).to_bytes(32, byteorder='big')
        else:
            raise TypeError("Seed must be a bytes object or a non-negative integer.")
            
        self.__counter = 0
        self.__randmax = 2**256 - 1
        self.__counter_max = 2**256 - 1
        self.__max_steps = 2**128
        
    def duplicate(self):
        return copy.deepcopy(self)
    
    def __generate_random_bytes(self):
        # Compute the SHA-3-256 hash
        hash_output = hashlib.sha3_256(b'prng_stream' + self.__key + self.__counter.to_bytes(32, byteorder='big')).digest()
        
        # Increment the counter
        self.__counter += 1
        if self.__counter > self.__counter_max:
            self.__counter = 0
        
        return hash_output
        
    def __generate_random_number(self):
        return int.from_bytes(self.__generate_random_bytes(), byteorder='big')
        
    def advance(self, steps):
        if not isinstance(steps, int) or steps <= 0:
            raise ValueError("Number of steps to advance must be a non-negative integer.")
        if steps > self.__max_steps:
            raise ValueError("Number of steps is too large. Maximum is 2^128 steps.")
            
        self.__counter = (self.__counter + steps) % (self.__randmax + 1)
        return self
        
    def jumped(self):
        self.__counter = (self.__counter + self.__max_steps) % (self.__randmax + 1)
        return self
        
    def add_entropy(self, entropy = None):
        if entropy is None:
            generated_entropy = secrets.token_bytes(32)
            self.__key = hashlib.sha3_256(b'prng_entropy' + self.__key + generated_entropy).digest()
        elif isinstance(entropy, bytes):
            if len(entropy) != 32:
                raise ValueError("Bytes object must be 256-bits (32 bytes) long for the external entropy.")
            self.__key = hashlib.sha3_256(b'prng_entropy' + self.__key + entropy).digest()
        elif isinstance(entropy, int):
            if entropy > (2**256 - 1) or entropy < 0:
                raise ValueError("Entropy must be a non-negative integer not greater than 2^256-1.")
            entropy_bytes = int(entropy).to_bytes(32, byteorder='big')
            self.__key = hashlib.sha3_256(b'prng_entropy' + self.__key + entropy_bytes).digest()
        else:
            raise TypeError("Entropy must be a bytes object or a non-negative integer.")
        return self
        
    def get_counter(self):
        return self.__counter
            
    def randbytes(self, bytelength):
        if not isinstance(bytelength, int) or bytelength <= 0:
            raise ValueError("bytelength must be a non-negative integer.")
            
        number_of_calls = (bytelength + 31) // 32  # This effectively rounds up
        byte_chunks = []  # Use a list to collect chunks
        
        for i in range(number_of_calls):
            byte_chunks.append(self.__generate_random_bytes())
        
        return b''.join(byte_chunks)[:bytelength]  # Join chunks at once
        
    def randint(self, lower_bound = 0, upper_bound = (2**256 - 1), count = None):
        if not isinstance(lower_bound, int) or not isinstance(upper_bound, int):
            raise TypeError("Lower and upper bounds must be integers.")
        if count is not None and not isinstance(count, int):
            raise TypeError("Count must be an integer.")
        if lower_bound >= upper_bound:
            raise ValueError("Lower bound must be less than upper bound.")
        if count is not None and count <= 0:
            raise ValueError("Count must be a positive integer.")
        if upper_bound - lower_bound > self.__randmax:
            raise ValueError("Output range is too large.")
            
        range_size = upper_bound + 1 - lower_bound
        limit = self.__randmax - ((self.__randmax + 1) % range_size)
        def generate_randint():
            x = self.__generate_random_number()
            while x > limit:
                x = self.__generate_random_number()
            return (x % range_size + lower_bound)
        
        if count == None:
            return generate_randint()
        return [generate_randint() for _ in range(count)]
        
    def randfloat(self, lower_bound = 0.0, upper_bound = 1.0, count = None):
        if not isinstance(lower_bound, (int, float)) or not isinstance(upper_bound, (int, float)):
            raise TypeError("Lower and upper bounds must be numbers.")
        if count is not None and not isinstance(count, int):
            raise TypeError("Count must be an integer.")
        if lower_bound >= upper_bound:
            raise ValueError("Lower bound must be less than upper bound.")
        if count is not None and count <= 0:
            raise ValueError("Count must be a positive integer.")
        if upper_bound - lower_bound > self.__randmax:
            raise ValueError("Output range is too large.")
            
        if count == None:
            return ((self.__generate_random_number() / self.__randmax) * (upper_bound - lower_bound) + lower_bound) * 1.0
        return [((self.__generate_random_number() / self.__randmax) * (upper_bound - lower_bound) + lower_bound) * 1.0 for _ in range(count)]

