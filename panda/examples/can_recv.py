import argparse
import time

from panda import Panda


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Print CAN traffic without enabling transmission.")
  parser.add_argument("--serial", help="select a panda by serial number")
  args = parser.parse_args()

  with Panda(serial=args.serial) as panda:
    print("Listening for CAN messages. Ctrl-C to exit.", flush=True)
    try:
      while True:
        messages = panda.can_recv()
        for address, data, bus in messages:
          print(f"{bus}  {address:08X}  {data.hex(' ')}", flush=True)
        if not messages:
          time.sleep(0.01)
    except KeyboardInterrupt:
      pass
