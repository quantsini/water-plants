"""Adapted from https://pypi.python.org/pypi/ntplib/
"""

import socket
import ustruct as struct
import time
from ucollections import namedtuple
from micropython import const


__all__ = ['request']


# Epoch
# ESP8266:  2000-01-01 00:00:00 UTC
# NTP: 1900-01-01 00:00:00 UTC
_NTP_DELTA = const(3155673600)
_PACKET_FORMAT = "!BBBb11I"


_to_frac = lambda timestamp, n=32: int(abs(timestamp - int(timestamp)) * 2**n)
_to_time = lambda integ, frac, n=32: integ + float(frac)/2**n
ntp_to_system_time = lambda timestamp: timestamp - _NTP_DELTA
system_to_ntp_time = lambda timestamp: timestamp + _NTP_DELTA


class NTPPacket(namedtuple(
    '_NTPPacket',
    'version mode tx_timestamp leap stratum poll precision root_delay root_dispersion ref_id ref_timestamp orig_timestamp recv_timestamp dest_timestamp'
)):

    @property
    def offset(self) -> float:
        """offset"""
        return ((self.recv_timestamp - self.orig_timestamp) +
                (self.tx_timestamp - self.dest_timestamp))/2

    @property
    def delay(self) -> float:
        """round-trip delay"""
        return ((self.dest_timestamp - self.orig_timestamp) -
                (self.tx_timestamp - self.recv_timestamp))

    @property
    def tx_time(self) -> float:
        """Transmit timestamp in system time."""
        return ntp_to_system_time(self.tx_timestamp)

    @property
    def recv_time(self) -> float:
        """Receive timestamp in system time."""
        return ntp_to_system_time(self.recv_timestamp)

    @property
    def orig_time(self) -> float:
        """Originate timestamp in system time."""
        return ntp_to_system_time(self.orig_timestamp)

    @property
    def ref_time(self) -> float:
        """Reference timestamp in system time."""
        return ntp_to_system_time(self.ref_timestamp)

    @property
    def dest_time(self) -> float:
        """Destination timestamp in system time."""
        return ntp_to_system_time(self.dest_timestamp)


def request(host: str, version: int = 3, port: int = 123, timeout: int = 5) -> NTPPacket:
    """Query a NTP server.

    Parameters:
    host    -- server name/address
    version -- NTP version to use
    port    -- server port
    timeout -- timeout on socket operations

    Returns:
    NTPPacket object
    """
    # lookup server address
    addrinfo = socket.getaddrinfo(host, port)[0]
    family, sockaddr = addrinfo[0], addrinfo[4]

    # create the socket
    s = socket.socket(family, socket.SOCK_DGRAM)

    try:
        s.settimeout(timeout)

        # create the request packet - mode 3 is client
        query_packet = NTPPacket(
            mode=3,
            version=version,
            tx_timestamp=system_to_ntp_time(time.time()),
            leap=0,
            stratum=0,
            poll=0,
            precision=0,
            root_delay=0,
            root_dispersion=0,
            ref_id=0,
            ref_timestamp=0,
            orig_timestamp=0,
            recv_timestamp=0,
            dest_timestamp=None,
        )

        raw_data = struct.pack(_PACKET_FORMAT,
            (query_packet.leap << 6 | query_packet.version << 3 | query_packet.mode),
            query_packet.stratum,
            query_packet.poll,
            query_packet.precision,
            int(query_packet.root_delay) << 16 | _to_frac(query_packet.root_delay, 16),
            int(query_packet.root_dispersion) << 16 | _to_frac(query_packet.root_dispersion, 16),
            query_packet.ref_id,
            int(query_packet.ref_timestamp),
            _to_frac(query_packet.ref_timestamp),
            int(query_packet.orig_timestamp),
            _to_frac(query_packet.orig_timestamp),
            int(query_packet.recv_timestamp),
            _to_frac(query_packet.recv_timestamp),
            int(query_packet.tx_timestamp),
            _to_frac(query_packet.tx_timestamp))

        # send the request
        s.sendto(raw_data, sockaddr)

        # wait for the response - check the source address
        src_addr = None,
        while src_addr[0] != sockaddr[0]:
            response_packet, src_addr = s.recvfrom(256)

        # build the destination timestamp
        dest_timestamp = system_to_ntp_time(time.time())
    finally:
        s.close()

    unpacked = struct.unpack(_PACKET_FORMAT,
            response_packet[0:struct.calcsize(_PACKET_FORMAT)])

    # construct corresponding statistics
    return NTPPacket(
        leap = unpacked[0] >> 6 & 0x3,
        version = unpacked[0] >> 3 & 0x7,
        mode = unpacked[0] & 0x7,
        stratum = unpacked[1],
        poll = unpacked[2],
        precision = unpacked[3],
        root_delay = float(unpacked[4])/2**16,
        root_dispersion = float(unpacked[5])/2**16,
        ref_id = unpacked[6],
        ref_timestamp = _to_time(unpacked[7], unpacked[8]),
        orig_timestamp = _to_time(unpacked[9], unpacked[10]),
        recv_timestamp = _to_time(unpacked[11], unpacked[12]),
        tx_timestamp = _to_time(unpacked[13], unpacked[14]),
        dest_timestamp=dest_timestamp,
    )
