from pathlib import Path
import subprocess
import sys

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


ROOT = Path(__file__).resolve().parent
FIRMWARE = [f"board/obj/{name}" for project in ("panda_h7", "panda_jungle_h7", "body_h7")
            for name in (f"{project}.bin.signed", f"bootstub.{project}.bin")]
RESOURCES = ["board/health.h", "board/jungle/jungle_health.h", *FIRMWARE]


def build_firmware():
  # Git checkouts build from source; release sdists already contain the binaries.
  if (ROOT / "SConstruct").exists():
    subprocess.check_call([sys.executable, "-m", "SCons", *FIRMWARE], cwd=ROOT)
  for resource in RESOURCES:
    if not (ROOT / resource).is_file():
      raise FileNotFoundError(f"Missing package resource: {resource}. Build firmware with ./setup.sh && scons first.")


class BuildPy(build_py):
  def run(self):
    if self.editable_mode:
      return
    build_firmware()
    super().run()
    for resource in RESOURCES:
      target = Path(self.build_lib) / "panda" / resource
      target.parent.mkdir(parents=True, exist_ok=True)
      self.copy_file(str(ROOT / resource), str(target))


class Sdist(sdist):
  def run(self):
    build_firmware()
    super().run()


setup(cmdclass={"build_py": BuildPy, "sdist": Sdist})
