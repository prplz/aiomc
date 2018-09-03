import asyncio
import json
import time
from collections import namedtuple

from . import packets
from .io import MinecraftIO
from .protocol import MinecraftProtocol

PingResult = namedtuple('PingResult', ('json', 'latency'))


async def minecraft_ping(host, port, loop: asyncio.AbstractEventLoop = None) -> PingResult:
    conn = MinecraftProtocol(loop)
    await loop.create_connection(lambda: conn, host, port)

    conn.write_packet(packets.handshake(47, host, port))
    conn.write_packet(packets.request_status())
    await conn.drain()

    packet = MinecraftIO(await conn.read_packet())
    assert packet.read_varint() == 0
    status = packet.read_string()

    ping_id = int(time.time() * 1000)
    conn.write_packet(packets.ping(ping_id))
    await conn.drain()

    ping_send_time = loop.time()

    packet = MinecraftIO(await conn.read_packet())
    latency = int((loop.time() - ping_send_time) * 1000)
    assert packet.read_varint() == 1
    assert packet.read_ulong() == ping_id

    conn.writer.close()

    json_ = json.loads(status)

    return PingResult(json_, latency)
