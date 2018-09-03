import argparse
import asyncio

from aiomc import minecraft_ping, resolve_minecraft_server


def aiomc():
    parser = argparse.ArgumentParser()
    parser.add_argument('address')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    async def run():
        host, port = resolve_minecraft_server(args.address)

        print(f'Resolved to {host}:{port}')

        res = await minecraft_ping(host, port, loop)
        print(f'Reply: {res.json}')
        print(f'Latency: {res.latency}ms')

    loop.run_until_complete(run())
