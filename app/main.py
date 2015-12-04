from codec import ExpGolombCodec
from utils import entropy

def main():
    codec = ExpGolombCodec()
    encoded = codec.encode([0, 0, 0, 1, 2, 3, 0, 1, 0, 0, 4, 0, 0, 6, 0, 5, 0, 0, 0, 0])
    print encoded
    print codec.statistics

    decoded = codec.decode(encoded)
    print decoded
    
if __name__ == '__main__':
    main()
    
