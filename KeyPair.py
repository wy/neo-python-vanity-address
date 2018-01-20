#Generate Public Key from Private Key

# Optimised for speed by reducing amount of library bloat needed

# WIF: Human Readable private key e.g. 5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ
# PublicKeyReadable: Human readable public key

import os
import bitcoin
import base58
import hashlib # comes with standard python implementation
import binascii # comes with standard python implementation
from ECCurve import ECDSA
from UInt160 import UInt160 # useful representation used in bitcoin / NEO


def random_bytes(nBytes):
    return os.urandom(nBytes)


def setup_curve():
    """
    Setup the Elliptic curve parameters.
    """
    bitcoin.change_curve(
        115792089210356248762697446949407573530086143415290314195533631308867097853951,
        115792089210356248762697446949407573529996955224135760342422259061068512044369,
        115792089210356248762697446949407573530086143415290314195533631308867097853948,
        41058363725152142129326129780047268409114441015993725554835256314039467401291,
        48439561293906451759052585252797914202762949526041747995844080717082404635286,
        36134250956749795798585127919587881956611106672985015071877198253568414405109
    )

setup_curve()


class KeyPair():
    PublicKey = None
    PrivateKey = None

    def __str__(self):
        s = "Address: {}\n".format(self.GetAddress())
        s += "WIF: {}\n".format(self.Export())
        return s

    @staticmethod
    def scripthash_to_address(scripthash):
        """
        Convert a script hash to a public address.
        Args:
            scripthash (bytes):
        Returns:
            str: base58 encoded string representing the wallet address.
        """
        sb = bytearray(23) + scripthash
        c256 = hashlib.sha256(hashlib.sha256(scripthash).digest()).digest()[0:4]
        outb = sb + bytearray(c256)
        return base58.b58encode(bytes(outb))

    @property
    def WIF(self):
        """
                Export this KeyPair's private key in WIF format.
                Returns:
                    str: The key in wif format
                """
        data = bytearray(38)
        data[0] = 0x80
        data[1:33] = self.PrivateKey[0:32]
        data[33] = 0x01

        checksum = KeyPair.checksum_generator(data[0:34])
        data[34:38] = checksum[0:4]
        b58 = base58.b58encode(bytes(data))

        return b58

    @staticmethod
    def checksum_generator(msg):
        return hashlib.sha256(hashlib.sha256(msg).digest()).digest()

    @staticmethod
    def PrivateKeyFromWIF(wif):
        """
                Get the private key from a WIF key
                Args:
                    wif (str): The wif key
                Returns:
                    bytes: The private key
                """
        if wif is None or len(wif) is not 52:
            raise ValueError('Please provide a wif with a length of 52 bytes (LEN: {0:d})'.format(len(wif)))

        data = base58.b58decode(wif)
        checksum = hashlib.sha256(hashlib.sha256((data[0:34])).digest()).digest()[0:4]

        if checksum != data[34:]:
            raise ValueError("Invalid WIF Checksum!")

        return data[1:33]

    @staticmethod
    def ToScriptHash(data):
        """
        Get a script hash of the data.
        Args:
            data (bytes): data to hash.
            unhex (bool): (Default) True. Set to unhexlify the stream. Use when the bytes are not raw bytes; i.e. b'aabb'
        Returns:
            UInt160: script hash.
        """
        if len(data) > 1:
            data = binascii.unhexlify(data)
        return UInt160(data=binascii.unhexlify(bytes(KeyPair.hash160(data), encoding='utf-8')))

    @staticmethod
    def hash160(string):
        intermed = hashlib.sha256(string).digest()
        return hashlib.new('ripemd160', intermed).hexdigest()

    @staticmethod
    def scripthash_to_address(scripthash):
        """
        Convert a script hash to a public address.
        Args:
            scripthash (bytes):
        Returns:
            str: base58 encoded string representing the wallet address.
        """
        sb = bytearray([23]) + scripthash
        c256 = hashlib.sha256(hashlib.sha256(sb).digest()).digest()[0:4]
        outb = sb + bytearray(c256)
        return base58.b58encode(bytes(outb))


    def GetAddress(self):
        """
        Returns the public NEO address for this KeyPair
        Returns:
            str: The human readable Public Address from the public key
        """
        script = b'21' + self.PublicKey.encode_point(True) + b'ac'
        script_hash = KeyPair.ToScriptHash(script)
        address = KeyPair.scripthash_to_address(script_hash.Data)
        return address

    def __init__(self, priv_key=None):
        """
        Create an instance
        :param priv_key: a private key
        """

        if priv_key is None:
            priv_key = bytes(random_bytes(32))

        length = len(priv_key)

        if length != 32: # Just handle 32 byte version
            raise ValueError("Invalid private key length")

        self.PrivateKey = bytearray(priv_key[-32:]) #Get last 32 bytes

        try:
            pubkey_encoded_not_compressed = bitcoin.privkey_to_pubkey(priv_key)
        except Exception as e:
            raise Exception("Could not determine public key")

        if pubkey_encoded_not_compressed:
            pubkey_points = bitcoin.decode_pubkey(pubkey_encoded_not_compressed, 'bin')

            pubx = pubkey_points[0]
            puby = pubkey_points[1]
            edcsa = ECDSA.secp256r1()
            self.PublicKey = edcsa.Curve.point(pubx, puby)
