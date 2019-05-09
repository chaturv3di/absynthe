from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="absynthe",
    version="0.0.1",
    url="https://github.com/chaturv3di/absynthe/",
    license="Apache License 2.0",
    author="Namit Chaturvedi",
    description="A (branching) Behaviour Synthesizer",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License 2.0",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    )
