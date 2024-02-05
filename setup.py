from setuptools import setup, find_packages

setup(
    name='dataDisk',
    version='1.2.0',
    url='https://github.com/davitacols/dataDisk',
    packages=find_packages(),
    install_requires=[
        'concurrent.futures',
    ],
    extras_require={
        'data_processing': ['numpy', 'pandas'],
    },
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
