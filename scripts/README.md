To package freesteam for pypi:

* create a `build` directory
* `cd build && cmake ..`
* `cd python`
* copy `setup.py` from scripts to the actual python build directory
* copy `README.txt` from srcdir in the actual python build directory
* `python setup.py bdist_wheel` 

The whl package is created in the `dist` directory
