*Disclaimer: I am neither a cryptographer nor a security expert, so I cannot vouch for the security of using this implementation in cryptographic or security-sensitive applications. Please use at your own discretion and consider consulting a qualified expert for such use cases.*

# sha3prng
This is a Python implementation of a 512-bit PRNG constructed purely using the SHA3-512 hash function. Since the output of a high-quality secure hash function such as SHA-3 is indistinguishable from true randomness, it can be used for generating random numbers with higher quality randomness compared to conventional PRNGs such as Mersenne Twister, PCG, xoshiro/xoroshiro, etc.

# Example/Usage
```python
import sha3prng

# Initialize PRNG with a random seed.
prng_instance = sha3prng.prng()

# Initialize PRNG with a chosen seed (512-bit integer or bytes object).
prng_instance = sha3prng.prng(42)

# Generate a random integer between 1 and 100 (inclusive)
random_int = prng_instance.randint(1, 100)

# Generate a 50-element list of random integers between -5 and 10 (inclusive)
random_int_list = prng_instance.randint(-5, 10, 50)

# Generate a random floating-point number between 0.0 and 5.0 (inclusive)
random_float = prng_instance.randfloat(0.0, 5.0)

# Generate a 15-element list of random floating-point numbers between 5.3 and 18.0 (inclusive)
random_float_list = prng_instance.randfloat(5.3, 18.0, 15)

# Generate a random bytes object with length of 74 bytes
random_bytes = prng_instance.randbytes(74)

# Add random entropy to the PRNG in case backwards resistance is needed.
prng_instance.add_entropy()

# Add chosen entropy (512-bit integer or bytes object) to the PRNG in case backwards resistance is needed.
prng_instance.add_entropy(619)

```

