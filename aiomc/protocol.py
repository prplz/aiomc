import asyncio

from .io import MinecraftIO


class MinecraftProtocol(asyncio.StreamReaderProtocol):
    def __init__(self, loop=None):
        super().__init__(asyncio.StreamReader(), self._connected, loop)

    @property
    def reader(self) -> asyncio.StreamReader:
        return self._stream_reader

    @property
    def writer(self) -> asyncio.StreamWriter:
        return self._stream_writer

    def _connected(self, reader, writer):
        pass

    async def read_varint(self, size: int = 5) -> int:
        result = 0
        for i in range(size):
            data = await self.reader.readexactly(1)
            shift = 7 * i
            result |= (data[0] & 0x7F) << shift
            if data[0] >> 7 == 0:
                return result
        else:
            raise ValueError(f'Varnum was too big, expected {size}')

    async def read_packet(self) -> bytes:
        length = await self.read_varint()
        packet = await self.reader.readexactly(length)
        return packet

    def write_packet(self, packet: bytes):
        header = MinecraftIO()
        header.write_varint(len(packet))
        packet = header.getvalue() + packet
        self.writer.write(packet)

    async def drain(self):
        await self.writer.drain()
