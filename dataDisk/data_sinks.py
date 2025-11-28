import logging
import os
import pandas as pd
import sqlite3
from typing import Optional, Dict, Any, Union, List


class DataSink:
    """Base class for all data sinks."""
    
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save data to the sink.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement this method")


class CSVSink(DataSink):
    """Sink for saving data to CSV files."""
    
    def __init__(self, file_path: str, **kwargs):
        """
        Initialize CSV sink.
        
        Args:
            file_path: Path to save the CSV file
            **kwargs: Additional arguments to pass to pandas to_csv
        """
        self.file_path = file_path
        self.kwargs = kwargs
        
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to CSV.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
            
        Raises:
            Exception: If saving fails
        """
        try:
            logging.info(f"Saving data to {self.file_path}")
            # Set default parameters if not provided
            kwargs = {'index': False}
            kwargs.update(self.kwargs)
            data.to_csv(self.file_path, **kwargs)
            logging.info("Data saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving data to CSV: {str(e)}")
            raise


class JSONSink(DataSink):
    """Sink for saving data to JSON files."""
    
    def __init__(self, file_path: str, orient: str = 'records', **kwargs):
        """
        Initialize JSON sink.
        
        Args:
            file_path: Path to save the JSON file
            orient: JSON orientation format
            **kwargs: Additional arguments to pass to pandas to_json
        """
        self.file_path = file_path
        self.orient = orient
        self.kwargs = kwargs
        
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to JSON.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
            
        Raises:
            Exception: If saving fails
        """
        try:
            logging.info(f"Saving data to {self.file_path}")
            kwargs = {'orient': self.orient}
            kwargs.update(self.kwargs)
            data.to_json(self.file_path, **kwargs)
            logging.info("Data saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving data to JSON: {str(e)}")
            raise


class SQLSink(DataSink):
    """Sink for saving data to SQL databases."""
    
    def __init__(self, db_path: str, table_name: str, if_exists: str = 'replace', **kwargs):
        """
        Initialize SQL sink.
        
        Args:
            db_path: Path to SQLite database
            table_name: Name of the table to save data to
            if_exists: How to behave if the table exists ('fail', 'replace', or 'append')
            **kwargs: Additional arguments to pass to pandas to_sql
        """
        self.db_path = db_path
        self.table_name = table_name
        self.if_exists = if_exists
        self.kwargs = kwargs
        
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to SQLite database.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
            
        Raises:
            Exception: If saving fails
        """
        try:
            logging.info(f"Saving data to SQLite database {self.db_path}, table {self.table_name}")
            conn = sqlite3.connect(self.db_path)
            kwargs = {'if_exists': self.if_exists, 'index': False}
            kwargs.update(self.kwargs)
            data.to_sql(self.table_name, conn, **kwargs)
            conn.close()
            logging.info("Data saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving data to SQLite: {str(e)}")
            raise


class ExcelSink(DataSink):
    """Sink for saving data to Excel files."""
    
    def __init__(self, file_path: str, sheet_name: str = 'Sheet1', **kwargs):
        """
        Initialize Excel sink.
        
        Args:
            file_path: Path to save the Excel file
            sheet_name: Name of the sheet to save data to
            **kwargs: Additional arguments to pass to pandas to_excel
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.kwargs = kwargs
        
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to Excel.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
            
        Raises:
            Exception: If saving fails
        """
        try:
            logging.info(f"Saving data to Excel file {self.file_path}, sheet {self.sheet_name}")
            kwargs = {'sheet_name': self.sheet_name, 'index': False}
            kwargs.update(self.kwargs)
            data.to_excel(self.file_path, **kwargs)
            logging.info("Data saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving data to Excel: {str(e)}")
            raise


class ParquetSink(DataSink):
    """Sink for saving data to Parquet files."""
    
    def __init__(self, file_path: str, compression: str = 'snappy', **kwargs):
        """
        Initialize Parquet sink.
        
        Args:
            file_path: Path to save the Parquet file
            compression: Compression algorithm to use
            **kwargs: Additional arguments to pass to pandas to_parquet
        """
        self.file_path = file_path
        self.compression = compression
        self.kwargs = kwargs
        
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to Parquet.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
            
        Raises:
            Exception: If saving fails
        """
        try:
            logging.info(f"Saving data to Parquet file {self.file_path}")
            kwargs = {'compression': self.compression}
            kwargs.update(self.kwargs)
            data.to_parquet(self.file_path, **kwargs)
            logging.info("Data saved successfully")
            return True
        except Exception as e:
            logging.error(f"Error saving data to Parquet: {str(e)}")
            raise


class MultiSink(DataSink):
    """Sink that saves data to multiple sinks."""
    
    def __init__(self, sinks: List[DataSink]):
        """
        Initialize MultiSink.
        
        Args:
            sinks: List of DataSink objects to save data to
        """
        self.sinks = sinks
        
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to all configured sinks.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if all saves were successful
            
        Raises:
            Exception: If any save fails
        """
        results = []
        errors = []
        
        for sink in self.sinks:
            try:
                result = sink.save(data)
                results.append(result)
            except Exception as e:
                errors.append(str(e))
                
        if errors:
            error_msg = "; ".join(errors)
            logging.error(f"Errors in MultiSink: {error_msg}")
            raise Exception(f"MultiSink encountered errors: {error_msg}")
            
        return all(results)
