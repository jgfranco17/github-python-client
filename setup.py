"""
Python setup for client package
"""
import io
import os

from setuptools import find_packages, setup


def __read_file(*paths, **kwargs):
    """
    Read the contents of a text file safely.
    """
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as file:
        content = file.read().strip()
    return content


def read_requirements(path):
    """
    Read the dependencies as a list from the file.
    """
    return [
        line.strip()
        for line in __read_file(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="gitclient",
    version=__read_file("gitclient", "VERSION"),
    description="Github API client",
    url="https://github.com/jgfranco17/github-python-client/",
    license="MIT",
    long_description=__read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Joaquin Franco",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
)
