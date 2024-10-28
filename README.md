*Disclaimer: im neither a cryptographer nor a security expert so i can't vouch for the security of using this in cryptographic/security applications.*

# sha3prng
This is a python implementation of a PRNG constructed purely using SHA3-512 hash function. Since the output of a high-quality secure hash function such as SHA-3 is indistinguishable from true randomness, it can be used for generating high quality random numbers.

# Usage
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

# Generate a 15-element list of random floating-point numbers between 5.5 and 18.0 (inclusive)
random_float_list = prng_instance.randfloat(5.5, 18.0, 15)

# Add random entropy to the PRNG in case backwards resistance is needed.
prng_instance.add_entropy()

# Add chosen entropy (512-bit integer or bytes object) to the PRNG in case backwards resistance is needed.
prng_instance.add_entropy(619)

```

