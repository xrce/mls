from setuptools import setup, find_packages
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_d = f.read()

setup(
    name='movielinkscraper',
    version='0.1.8',
    description='Simple tool for scraping movie links from any site',
    long_description=long_d,
    long_description_content_type="text/markdown",
    author='Your Future Boyfriend',
    author_email='n1ghtpe0ple@protonmail.com',
    url='https://github.com/xrce/mls',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    install_requires=["requests", "argparse", "prettytable", "beautifulsoup4", "selenium"],
)