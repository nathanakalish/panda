"""Only source checkouts need the firmware compiler; sdists carry prebuilt firmware."""
from pathlib import Path
import tomllib

from setuptools.build_meta import (  # noqa: F401
  build_editable, build_sdist, build_wheel, get_requires_for_build_editable,
  prepare_metadata_for_build_editable, prepare_metadata_for_build_wheel,
)
from setuptools import build_meta


def firmware_requirements():
  root = Path(__file__).resolve().parent
  if not (root / "SConstruct").exists():
    return []
  config = tomllib.loads((root / "pyproject.toml").read_text())
  return ["scons", *[dep for dep in config["dependency-groups"]["firmware"] if not dep.startswith("cppcheck")]]


def get_requires_for_build_wheel(config_settings=None):
  return build_meta.get_requires_for_build_wheel(config_settings) + firmware_requirements()


def get_requires_for_build_sdist(config_settings=None):
  return build_meta.get_requires_for_build_sdist(config_settings) + firmware_requirements()
