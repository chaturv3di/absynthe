import imp
import os
from setuptools import setup, find_packages

version = imp.load_source(
    'absynthe.version', os.path.join('absynthe', 'version.py')).VERSION

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="absynthe",
    version=version,
    url="https://github.com/chaturv3di/absynthe/",
    license="Apache License 2.0",
    author="Namit Chaturvedi",
    description="A (branching) Behaviour Synthesizer",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: Log Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    python_requires=">=3.6.0",
    )
