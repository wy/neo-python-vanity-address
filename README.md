# neo-python-vanity-address
Python generator for vanity addresses

This allows you to quickly and easily generate public addresses that contain substrings that you would like to have.

```
> python3 VanityAddress.py [-c] substring
- Generates NEO addresses that contain your desired substring. Use -c if you want case sensitivity or leave it out if not.
```

=== Brief Explanation ===

It is not possible to directly generate a public address due to the way that the NEO/Bitcoin-based security works. Instead, you first randomly generate private keys. Each private key corresponds to a public key and a public address.

So it is a brute force method that repeatedly generates public addresses and then checks if the address matches your specific requirement.

The script needs no online access (so can be run on an airgapped machine) and will output to console as well as write to a log file any matches.

The script will output the public address as well as the WIF (wallet import format) which is based on the private key. You can use this WIF with Neon Wallet or any other wallet to control this address.

=== Security and Speed ===

Where possible, I have tried not to import libraries unnecessarily. In the latest version you will need to pip install the following libraries:
- bitcoin - this is a library for applying the cryptographic process (shared with bitcoin and NEO)
- base58 - a helper library for dealing with base58 strings
- mpmath - fixed point math
- logzero - logging debug (I could probably edit this out)

```
> pip3 install bitcoin
> pip3 install base58
> pip3 install mpmath
> pip3 install logzero
```

For security reasons, you should audit the code to be confident there is no access online to any data being produced. As there are very few python files and only two external non-library imports, this should be easy to do.

For speed reasons, I have taken some inspiration from the NEO python client libraries but removed functions that were overly general for this specific needs. There is more than can be done.

I have tested this on pythonanywhere as well as on my local machine (Windows 10 i5 core), and it can produce and test 10,000 candidate addresses in about 40 seconds.
