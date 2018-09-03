import io
import struct


class MinecraftIO(io.BytesIO):
    def read_varint(self, size: int = 5) -> int:
        result = 0
        for i in range(size):
            data = self.read(1)
            shift = 7 * i
            result |= (data[0] & 0x7F) << shift
            if data[0] >> 7 == 0:
                return result
        else:
            raise ValueError(f'Varnum was too big, expected {size}')

    def write_varint(self, value: int):
        while value > 0x7F:
            self.write(bytes([value & 0x7F | 0x80]))
            value >>= 7
        self.write(bytes([value]))

    def read_string(self) -> str:
        length = self.read_varint()
        data = self.read(length)
        return data.decode('utf-8')

    def write_string(self, value: str):
        value_data = value.encode('utf-8')
        self.write_varint(len(value_data))
        self.write(value_data)

    def write_ushort(self, value: int):
        self.write(struct.pack('H', value))

    def read_ulong(self) -> int:
        data = self.read(8)
        return struct.unpack('Q', data)[0]

    def write_ulong(self, value: int):
        self.write(struct.pack('Q', value))
