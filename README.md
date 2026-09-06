# Welcome to panda

[![PyPI](https://img.shields.io/pypi/v/pandacan)](https://pypi.org/project/pandacan/)

panda speaks CAN and CAN FD, and it runs on the [STM32H725](https://www.st.com/resource/en/reference_manual/rm0468-stm32h723733-stm32h725735-and-stm32h730-value-line-advanced-armbased-32bit-mcus-stmicroelectronics.pdf).

## Directory structure

```
.
├── board           # Code that runs on the STM32
├── panda           # Python library, including runnable examples
├── tests           # Tests for panda
└── scripts         # Miscellaneous used for panda development and debugging
```

## Safety Model

panda is compiled with vehicle-specific safety logic provided by [opendbc](https://github.com/commaai/opendbc). See details about the car safety models, safety testing, and code rigor in that repository.

## Code Rigor

The panda firmware is written for its use in conjunction with [openpilot](https://github.com/commaai/openpilot). The panda firmware, through its safety model, provides and enforces the
[openpilot safety](https://github.com/commaai/openpilot/blob/master/docs/SAFETY.md). Due to its critical function, it's important that the application code rigor within the `board` folder is held to high standards.

These are the [CI regression tests](https://github.com/commaai/panda/actions) we have in place:
* A generic static code analysis is performed by [cppcheck](https://github.com/danmar/cppcheck/).
* In addition, [cppcheck](https://github.com/danmar/cppcheck/) has a specific addon to check for [MISRA C:2012](https://misra.org.uk/) violations. See [current coverage](https://github.com/commaai/panda/blob/master/tests/misra/coverage_table).
* Compiler options are strict: the flags `-Wall -Wextra -Wstrict-prototypes -Werror` are enforced.
* The [safety logic](https://github.com/commaai/panda/tree/master/opendbc/safety) is tested and verified by [unit tests](https://github.com/commaai/panda/tree/master/opendbc/safety/tests) for each supported car variant to ensure that the behavior remains unchanged.
* A hardware-in-the-loop test verifies panda's functionalities on all active panda variants, including:
  * additional safety model checks
  * compiling and flashing the bootstub and app code
  * receiving, sending, and forwarding CAN messages on all buses
  * CAN loopback and latency tests through SPI

The above tests are themselves tested by:
* a [mutation test](tests/misra/test_mutation.py) on the MISRA coverage
* a [mutation test]([tests/misra/test_mutation.py](https://github.com/commaai/opendbc/blob/master/opendbc/safety/tests/mutation.sh)) on the vehicle-specific safety logic

## Usage

Install with Python 3.11 or 3.12 on Linux, macOS, or Windows:

```bash
python -m pip install pandacan
python -m panda list           # list connected devices
python -m panda health         # firmware version and health
```

The package includes the Python library, examples, and firmware for panda, jungle, and body. See [the Panda class](https://github.com/commaai/panda/blob/master/panda/panda.py) for the full API.

For example, to receive CAN messages:
``` python
>>> from panda import Panda
>>> panda = Panda()
>>> panda.can_recv()
```
And to send one on bus 0:
``` python
>>> from opendbc.car.structs import CarParams
>>> panda.set_safety_mode(CarParams.SafetyModel.allOutput)
>>> panda.can_send(0x1aa, b'message', 0)
```
Use `allOutput` only on a disconnected test bench; vehicle integrations should use the appropriate vehicle-specific safety model.

Run the included examples without a checkout:

```bash
python -m panda.examples.can_recv
python -m panda.examples.can_logger --output drive.csv
```

Both examples receive without enabling transmission. Use `--serial SERIAL` to select a device, or `--help` for options. More examples are in [panda/examples](https://github.com/commaai/panda/tree/master/panda/examples).

Update a panda with `python -m panda flash` or `Panda().flash()`. The package includes debug-signed development firmware and bootstubs; flashing and recovery need no compiler. `PandaJungle().flash()` uses jungle firmware. Pass `os.path.join(FW_PATH, "body_h7.bin.signed")` to `PandaBody.flash(fn=...)` for body firmware. Openpilot manages its own firmware updates.

Note that you may have to setup [udev rules](https://github.com/commaai/panda/tree/master/drivers/linux) for Linux, such as
``` bash
sudo tee /etc/udev/rules.d/11-panda.rules <<EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="3801", ATTRS{idProduct}=="ddcc", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="3801", ATTRS{idProduct}=="ddee", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="bbaa", ATTRS{idProduct}=="ddcc", MODE="0666"
SUBSYSTEM=="usb", ATTRS{idVendor}=="bbaa", ATTRS{idProduct}=="ddee", MODE="0666"
EOF
sudo udevadm control --reload-rules && sudo udevadm trigger
```

The panda jungle uses different udev rules. See [the repo](https://github.com/commaai/panda_jungle#udev-rules) for instructions.

## Development

```bash
git clone https://github.com/commaai/panda.git
cd panda
./setup.sh  # editable install and development dependencies
./test.sh   # build firmware, lint, and run tests
uv build --python 3.12  # build wheel and source archive with firmware
```

Installing from Git also builds firmware and downloads the ARM toolchain (Linux and macOS):

```bash
python -m pip install git+https://github.com/commaai/panda.git
```

## Licensing

panda software is released under the MIT license unless otherwise specified.
