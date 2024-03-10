import zlib
import binascii

def main():
    hexstring = input("Please enter a hexadecimal string: ")

    try:
        # Convert hexadecimal string to bytes
        blob = bytes.fromhex(hexstring)
    except ValueError:
        print("Invalid hexadecimal string")
        return 1

    try:
        # Get uncompressed data length from the first 4 bytes
        uncompressed_length = int.from_bytes(blob[:4], byteorder='big')
        # Decompress the data
        uncompressed = zlib.decompress(blob[4:])
    except zlib.error:
        print("Corrupt input, unable to uncompress")
        return 1
    
    # Print hexdump of the uncompressed buffer
    print(binascii.hexlify(uncompressed).decode())

if __name__ == "__main__":
    main()