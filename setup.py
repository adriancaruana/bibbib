import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="bibbib",
    version="0.0.1",
    description="bibbib - A Simple BiBTeX linter.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/adriancaruana/bibbib",
    author="Adrian Caruana",
    author_email="adrian@adriancaruana.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["bibbib"],
    keywords=["BiBTeX", "linter", "validator"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "bibtexparser",
    ],
    entry_points={
        "console_scripts": [
            "bibbib=bibbib.bibbib:bibbib",
        ]
    },
)
