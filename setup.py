from setuptools import setup, find_packages

setup(
    name='dataDisk',
    version='1.1.0',
    url='https://github.com/davitacols/DataFlow',
    packages=find_packages(),
    install_requires=[
        'concurrent.futures',
        'multiprocessing',
    ],
    extras_require={
        'data_processing': ['numpy', 'pandas'],
    },
)
