# Simulation Game
[![Build Status](https://travis-ci.org/olehermanse/sim_game.svg?branch=master)](https://travis-ci.org/olehermanse/sim_game)

## Installation
### Unix
Make sure you have python3 and pip3 correctly installed.
You can use a [virtual environment](https://docs.python.org/3/library/venv.html), if you like.
Install dependencies using:
```
pip3 install -U pip wheel
pip3 install -r requirements.txt
```

Sometimes, life is not so simple;
See how installation on different platforms is done in travis: [install.sh](./travis/install.sh)

### Windows
Multiple installations/versions of python can be troublesome on windows.
If you don't know what you're doing, uninstall all other versions of python.
Otherwise, always make sure you are using the correct installation of python AND pip.
If you do need multiple installations, use the [py launcher](https://docs.python.org/dev/using/windows.html#from-the-command-line) to run all commands (including pip).

Recommended Python version 3.5, 64 bit from:
https://www.python.org/downloads/windows/

The windows installers will name the python 3 executable `python.exe`.
Thus, you should be able to type `python` in cmd to use python 3.
Writing `python3` in cmd will not work (by default), however `pip3` will.

Download pre-built libraries(wheels) from this site:
http://www.lfd.uci.edu/~gohlke/pythonlibs/

If python, pip and ensurepip are all up to date, all you have to do is download the wheel file and:
```
pip3 install filename.whl
```

Example:
```
pip3 install ./pyglet‑1.2.4‑py3‑none‑any.whl
```

More comprehensive guide:
https://www.webucator.com/blog/2015/03/installing-the-windows-64-bit-version-of-pygame/
