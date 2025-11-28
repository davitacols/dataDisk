from setuptools import setup, find_packages

with open("Readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dataDisk',
    version='1.2.0',
    url='https://github.com/davitacols/dataDisk',
    author='David Ansa',
    author_email='davitacols@gmail.com',
    description='A Python package for data processing pipelines',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.0',
        'pandas>=1.0.0',
        'scikit-learn>=1.0.0',
    ],
    extras_require={
        'dev': ['pytest>=6.0.0', 'flake8>=3.8.0', 'black>=22.0.0', 'isort>=5.0.0'],
        'excel': ['openpyxl>=3.0.0'],
        'sql': ['sqlalchemy>=1.4.0'],
    },
    python_requires='>=3.7',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)
