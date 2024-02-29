from setuptools import setup, find_packages

setup(
    name='movielinkscraper',
    version='0.1.5',
    description='Simple tool for scraping movie links from any site',
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