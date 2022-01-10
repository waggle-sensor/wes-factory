import argparse
import fcntl
import logging
import socket
import struct
import time
from os import getenv

from waggle.plugin import Plugin


def publish_interface_ip(args, intf):
    """Publish the interface IP address

    Args:
        args: all program arguments
        intf: interface to collect and publish the IP info
    """

    logging.info("collecting interface (%s) IP address", intf)

    try:
        # do the core work to get the IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(
            fcntl.ioctl(
                s.fileno(),
                # SIOCGIFADDR
                0x8915,
                struct.pack("256s", bytes(intf[:15], "utf-8")),
            )[20:24]
        )
        with Plugin() as plugin:
            plugin.publish("sys.net.ip", ip, meta={"device": intf}, scope=args.scope)
            logging.info("published interface (%s) IP (%s)", intf, ip)
    except Exception:
        logging.exception("failed to add interface (%s) IP", intf)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logs")
    parser.add_argument(
        "--scope", default="all", choices=["all", "node", "beehive"], help="publish scope"
    )
    parser.add_argument(
        "--interfaces",
        default=getenv("INTERFACES", "wan0,wifi0,modem0"),
        help="hosts interfaces to publish IP info",
    )
    parser.add_argument(
        "--collect-interval",
        default=float(getenv("COLLECT_INTERVAL", "60.0")),
        type=float,
        help="interval in seconds to collect data and publish",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    logging.info("collecting factory data every %s seconds", args.collect_interval)
    while True:
        for intf in args.interfaces.split(","):
            intf = intf.lower()
            try:
                publish_interface_ip(args, intf)
            except Exception:
                logging.warning("failed to add interface (%s)", intf)

        time.sleep(args.collect_interval)


if __name__ == "__main__":
    main()
