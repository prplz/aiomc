import random
from ipaddress import AddressValueError, IPv4Address
from typing import Tuple

from dns import resolver
from dns.exception import DNSException


def resolve_minecraft_server(address) -> Tuple[str, int]:
    host = address
    port = None

    if ':' in address:
        parts = address.split(':')
        if len(parts) > 2:
            raise ValueError("Invalid address '%s'" % address)
        host = parts[0]
        port = int(parts[1])

    # if no port is supplied use 25565 or an SRV record if it exists
    if port is None:
        port = 25565

        # attempt to find an SRV record for this host
        try:
            answers = resolver.query('_minecraft._tcp.' + host, 'SRV')
            if answers:
                answer = answers[0]
                host = str(answer.target).rstrip(".")
                port = int(answer.port)
        except DNSException:
            pass

    # return address pair if host is a valid IPv4 address
    try:
        IPv4Address(host)
        return host, port
    except AddressValueError:
        pass

    # pick a random A record for this host
    answer = random.choice(resolver.query(host, 'A'))
    return answer.address, port
