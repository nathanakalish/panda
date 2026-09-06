import argparse
import csv
import time

from panda import Panda


def can_logger(serial=None, output="output.csv"):
  with Panda(serial=serial) as panda, open(output, "w", newline="") as stream:
    writer = csv.writer(stream)
    writer.writerow(["Bus", "MessageID", "Message", "MessageLength", "Time"])
    print(f"Writing CAN messages to {output}. Ctrl-C to exit.", flush=True)
    start = time.monotonic()
    count = 0
    try:
      while True:
        messages = panda.can_recv()
        for address, data, bus in messages:
          writer.writerow([bus, hex(address), f"0x{data.hex()}", len(data), time.monotonic() - start])
          count += 1
        if not messages:
          time.sleep(0.01)
    except KeyboardInterrupt:
      print(f"Saved {count} messages to {output}.")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Record CAN traffic to CSV without enabling transmission.")
  parser.add_argument("--serial", help="select a panda by serial number")
  parser.add_argument("--output", default="output.csv", help="CSV output path (default: %(default)s)")
  args = parser.parse_args()
  can_logger(args.serial, args.output)
