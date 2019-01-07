import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="RiskMan",
    version="0.1build_18.01.07",
    author="Zero Substance Trading",
    author_email="pentsok@zerosubstance.org",
    description=("A utility to display the number of shares of a stock to purchase"
                 "to purchase based on a set dolar risk amount and a list of stop values."),
    license="GPL",
    keywords="stock trading utility",
    url="http://zerosubstance.org/RiskMan",
    packages=['riskman'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Trading Utilities",
        "License :: GPLv3 License",
    ],
)
