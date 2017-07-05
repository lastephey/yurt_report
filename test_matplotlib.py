#! python

import matplotlib as mpl

print("config directory")
print(mpl.get_configdir())

print("install directory")
print(mpl.__file__)

print("cache directory")
print(mpl.get_cachedir())