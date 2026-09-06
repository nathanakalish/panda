"""Run against a wheel or sdist installed in a fresh environment outside the checkout."""
import importlib
from importlib.metadata import distribution
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import panda
from panda import Panda, PandaBody, PandaDFU, PandaJungle, PandaJungleDFU, PandaSerial, FW_PATH, pack_can_buffer, unpack_can_buffer


class TestInstalledPackage(unittest.TestCase):
  def test_install_location(self):
    self.assertNotIn(Path(__file__).resolve().parents[2], Path(panda.__file__).resolve().parents)

  def test_resources(self):
    for project in ("panda_h7", "panda_jungle_h7", "body_h7"):
      for name in (f"{project}.bin.signed", f"bootstub.{project}.bin"):
        self.assertGreater((Path(FW_PATH) / name).stat().st_size, 128)
    self.assertGreater(Panda.HEALTH_STRUCT.size, 0)
    self.assertGreater(PandaJungle.HEALTH_STRUCT.size, 0)
    self.assertTrue(issubclass(PandaBody, Panda))
    self.assertTrue(issubclass(PandaJungleDFU, PandaDFU))
    self.assertTrue(callable(PandaSerial))

  def test_can_roundtrip(self):
    messages = [(0x123, b"hello", 0), (0x18DA10F1, bytes(range(64)), 2)]
    decoded, remaining = unpack_can_buffer(b"".join(pack_can_buffer(messages, fd=True)))
    self.assertEqual(decoded, messages)
    self.assertEqual(remaining, b"")

  def test_dfu_uses_bundled_bootstub(self):
    for cls in (PandaDFU, PandaJungleDFU):
      dfu = object.__new__(cls)
      dfu._mcu_type = panda.McuType.H7
      with patch.object(dfu, "program_bootstub") as program, patch.object(dfu, "reset"):
        dfu.recover()
        self.assertGreater(len(program.call_args.args[0]), 128)

  def test_examples_and_cli(self):
    for name in ("can_recv", "can_logger", "can_unique", "can_bit_transition", "query_fw_versions", "query_vin_and_stats", "tesla_tester"):
      importlib.import_module(f"panda.examples.{name}")
    for module in ("panda", "panda.examples.can_recv", "panda.examples.can_logger", "panda.examples.query_fw_versions"):
      subprocess.run([sys.executable, "-m", module, "--help"], check=True, capture_output=True)

  def test_metadata(self):
    package = distribution("pandacan")
    self.assertFalse(any(" @ " in dep for dep in package.requires or []))


if __name__ == "__main__":
  unittest.main()
