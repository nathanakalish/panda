import argparse
import json

from panda import Panda, PandaDFU


def main():
  parser = argparse.ArgumentParser(description="Discover, inspect, and update a comma.ai panda over USB or SPI.")
  commands = parser.add_subparsers(dest="command", required=True)
  commands.add_parser("list", help="list connected panda and DFU serial numbers")
  for command, help_text in (("health", "print firmware version and health"), ("flash", "flash the bundled panda firmware")):
    subparser = commands.add_parser(command, help=help_text)
    subparser.add_argument("--serial", help="select a panda by serial number")
    if command == "flash":
      subparser.add_argument("--firmware", help="flash this file instead of the bundled firmware")
  args = parser.parse_args()

  if args.command == "list":
    print(json.dumps({"panda": Panda.list(), "dfu": PandaDFU.list()}, indent=2))
  else:
    with Panda(serial=args.serial) as panda:
      if args.command == "health":
        print(json.dumps({"version": panda.get_version(), "health": panda.health()}, indent=2))
      elif args.command == "flash":
        panda.flash(fn=args.firmware)


if __name__ == "__main__":
  main()
