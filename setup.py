"""Setuptools configuration for apyio."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst', 'r') as readmefile:

    README = readmefile.read()

setup(
    name='apyio',
    version='0.1.0',
    url='https://github.com/asyncdef/apyio',
    description='Async wrappers for standard Python io streams.',
    author="Kevin Conway",
    author_email="kevinjacobconway@gmail.com",
    long_description=README,
    license='Apache 2.0',
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [

        ],
    },
    include_package_data=True,
)
