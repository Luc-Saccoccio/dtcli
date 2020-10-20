import codecs
from setuptools import setup, find_packages
from dtcli import __version__, __author__, __email__


with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]


def long_description():
    with codecs.open('README.md', 'rb') as readme:
        return readme.read().decode('utf-8')

setup(
    name='dtcli',
    version=__version__,
    packages=find_packages(),

    author=__author__,
    author_email=__email__,
    keywords='dtc, nsf, bash.org, cli',
    description='DTC/NSF/bash.org cli querying tool',
    long_description=long_description(),
    url='https://github.com/Luc-Saccoccio/dtcli',

    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'dtcli = dtcli.command:main',
        ]
    },
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
    ],
)
