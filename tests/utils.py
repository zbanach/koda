from bitstream import BitStream

def make_bitstream(str):
    bools = [True if c == "1" else False for c in str]
    return BitStream(bools)
