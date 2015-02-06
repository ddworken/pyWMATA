from distutils.core import setup

description = open('README.md').read()

setup(name="pyWMATA",
      version='1.0',
      py_modules=["pyWMATA"],
      description="Python library to access WMATA's API. ",
      author="David Dworken",
      author_email = "david@daviddworken.com",
      license='GPLv2',
      url="https://github.com/ddworken/pyWMATA",
      long_description=description,
      platforms=["any"],
      )
