#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["pyparsing>=2.4.7<3"]

setup(
    author="Oscar David Arbeláez Echeverri",
    author_email="odarbelaeze@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Python bibtex parser and serializer.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="bibtext, parser",
    name="bibtexpy",
    packages=find_packages(where="src"),
    package_dir={"": "src/", "bibtexpy": "src/bibtexpy"},
    url="https://github.com/coreofscience/bibtexpy",
    version="0.0.1",
    zip_safe=False,
)
