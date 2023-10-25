from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='robowaiter',
    version='0.1.0',
    packages=['robowaiter'],
    install_requires=required,
    author='HPCL-EI',
    author_email='hpcl_ei@163.com',
    description='RoboWaiter',
    url='https://github.com/HPCL-EI/RoboWaiter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

