import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="freedeck-serial-api",
    version="0.2.0",
    description="A python lib to speak to the FreeDeck over serial",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/freeyourstream/freedeck-serial-api-python",
    author="Kilian Gosewisch",
    author_email="kilian2798@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["fdserial"],
    include_package_data=True,
    install_requires=["pyserial==3.5"],
    entry_points={
        "console_scripts": [
            "fdserialtest=fdserial.__main__:main",
        ]
    },
)
