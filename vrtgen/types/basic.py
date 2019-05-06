class Boolean(type):
    bits = 1
    def __new__(cls, value=False):
        return bool(value)

class IntegerType(int):
    __cached__ = {}

    def __new__(cls, value=0):
        value = int.__new__(cls, value)
        if value > cls.maxval:
            raise ValueError('{} cannot exceed {:d}'.format(cls.__name__, cls.maxval))
        elif value < cls.minval:
            raise ValueError('{} cannot be less than {:d}'.format(cls.__name__, cls.minval))
        return value

    def __init_subclass__(cls, bits, signed=True, **kwds):
        super().__init_subclass__(**kwds)
        cls.bits = bits
        cls.signed = signed
        if signed:
            cls.minval = -(2**(bits-1))
            cls.maxval = -cls.minval - 1
        else:
            cls.minval = 0
            cls.maxval = (2**bits) - 1

    @staticmethod
    def create(bits, signed=True):
        key = (bits, signed)
        existing = IntegerType.__cached__.get(key, None)
        if existing:
            return existing
        name = 'Int{:d}'.format(bits)
        if not signed:
            name = 'U'+name
        newclass = type(name, (IntegerType,), {}, bits=bits, signed=signed)
        IntegerType.__cached__[key] = newclass
        return newclass

class Integer64(IntegerType, bits=64): pass
class Integer32(IntegerType, bits=32): pass
class Integer24(IntegerType, bits=24): pass
class Integer16(IntegerType, bits=16): pass
class Integer8(IntegerType, bits=8): pass

class FixedPointType(float):
    __cached__ = {}

    def __new__(cls, value=0.0):
        value = float.__new__(cls, value)
        # TODO: range checking
        return value

    def __init_subclass__(cls, bits, radix, **kwds):
        super().__init_subclass__(**kwds)
        cls.bits = bits
        cls.radix = radix

    @staticmethod
    def create(bits, radix):
        key = (bits, radix)
        existing = FixedPointType.__cached__.get(key, None)
        if existing:
            return existing
        name = 'FixedPoint{:d}_{:d}'.format(bits, radix)
        newclass = type(name, (FixedPointType,), {}, bits=bits, radix=radix)
        FixedPointType.__cached__[key] = newclass
        return newclass


FixedPoint64_20 = FixedPointType.create(64, 20)
FixedPoint32_16 = FixedPointType.create(32, 16)
FixedPoint16_7 = FixedPointType.create(16, 7)
FixedPoint16_13 = FixedPointType.create(16, 13)

Identifier32 = Integer32
Identifier16 = Integer16

class StreamIdentifier(IntegerType, bits=32, signed=False): pass

class OUI(IntegerType, bits=24):
    pass
