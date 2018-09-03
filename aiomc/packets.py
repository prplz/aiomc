import struct

from .io import MinecraftIO


def handshake(version: int, address: str, port: int) -> bytes:
    packet = MinecraftIO()
    packet.write_varint(0)  # handshake id
    packet.write_varint(version)
    packet.write_string(address)
    packet.write_ushort(port)
    packet.write_varint(1)  # protocol 1 for status (ping)
    return packet.getvalue()


def request_status() -> bytes:
    return b'\x00'


def ping(ping_id) -> bytes:
    return b'\x01' + struct.pack('Q', ping_id)
