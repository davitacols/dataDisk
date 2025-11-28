"""
dataDisk - A Python package for data processing pipelines.

This package provides tools for creating and executing data processing pipelines,
applying transformations, validating data, and saving results.
"""

__version__ = "1.2.0"
__author__ = "David Ansa"

from .data_sources import (
    DataSource, CSVDataSource, SQLDataSource, JSONDataSource, 
    ExcelDataSource, ParquetDataSource
)
from .pipeline import DataPipeline
from .transformation import Transformation
from .validator import Validator, check_null, check_positive
from .parallel_processor import ParallelProcessor
from .data_sinks import (
    DataSink, CSVSink, JSONSink, SQLSink, ExcelSink, ParquetSink, MultiSink
)

__all__ = [
    "DataSource",
    "CSVDataSource",
    "SQLDataSource",
    "JSONDataSource",
    "ExcelDataSource",
    "ParquetDataSource",
    "DataPipeline",
    "Transformation",
    "Validator",
    "check_null",
    "check_positive",
    "ParallelProcessor",
    "DataSink",
    "CSVSink",
    "JSONSink",
    "SQLSink",
    "ExcelSink",
    "ParquetSink",
    "MultiSink",
]
