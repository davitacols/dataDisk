from setuptools import setup, find_packages

setup(
    name='dataflow',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'concurrent.futures',
        'multiprocessing',
    ],
    extras_require={
        'data_processing': ['numpy', 'pandas'],
    },
)
