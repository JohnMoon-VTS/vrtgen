# C++ VITA 49.2 Packet Generator

C++ support for `vrtgen`.
`vrtgen-cpp` comprises a Python plugin for `vrtgen` and a C++ header-only library.

This is a work-in-progress and almost assuredly will break repeatedly.

## Dependencies

The code generation plugin requires `vrtgen`.
No additional dependencies are required.

Generated C++ code requires C++11 support.
The only dependency is the C++ header library.

To build the C++ header library, CMake 3.13 must be installed.

## Installation

The Python plugin must be installed to generate the C++ headers.

To install the Python plugin:

```sh
pip3 install .
```

Then, to build the C++ library:

```sh
cmake -B build
cd build
make install
```

On some Linux systems, such as CentOS 7, you must explicitly run `cmake3` instead of `cmake`.

The headers are installed to `/usr/local/include/vrtgen` by default.

## Usage

The `vrtpktgen` program automatically discovers registered code generator plugins.
To generate C++ bindings from your YAML specification:

```sh
vrtpktgen -b cpp <yaml file>
```

This will generate `.hpp` and `.cpp` files with the same basename as the input file.

## Developer Setup

To perform a "developer install":

```sh
pip3 install -e .
```

This will create a link to your project in the Python `site-packages` directory.
It is strongly recommended to use a `venv` environment or Docker image for development.