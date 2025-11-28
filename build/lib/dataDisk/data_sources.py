import pandas as pd
import logging
import sqlite3
import os
import json
from typing import Optional, Dict, Any, Union, List


class DataSource:
    """Base class for all data sources."""
    
    def load(self) -> pd.DataFrame:
        """
        Load data from the source.
        
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def save(self, data: pd.DataFrame) -> bool:
        """
        Save data to the source.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses should implement this method.")


class CSVDataSource(DataSource):
    """Source for loading and saving CSV data."""
    
    def __init__(self, file_path: str, **kwargs):
        """
        Initialize CSV data source.
        
        Args:
            file_path: Path to the CSV file
            **kwargs: Additional arguments to pass to pandas read_csv/to_csv
        """
        self.file_path = file_path
        self.kwargs = kwargs
        
    def load(self) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        try:
            logging.info(f"Loading data from {self.file_path}")
            data = pd.read_csv(self.file_path, **self.kwargs)
            return data
        except Exception as e:
            logging.error(f"Error loading data from CSV: {str(e)}")
            raise
            
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to CSV.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
        """
        try:
            logging.info(f"Saving data to {self.file_path}")
            # Set default parameters if not provided
            kwargs = {'index': False}
            kwargs.update(self.kwargs)
            data.to_csv(self.file_path, **kwargs)
            return True
        except Exception as e:
            logging.error(f"Error saving data to CSV: {str(e)}")
            raise


class SQLDataSource(DataSource):
    """Source for loading and saving SQL data."""
    
    def __init__(self, db_filepath: str, table_name: str = 'results', **kwargs):
        """
        Initialize SQL data source.
        
        Args:
            db_filepath: Path to SQLite database
            table_name: Name of the table to load/save data from/to
            **kwargs: Additional arguments to pass to pandas read_sql_query/to_sql
        """
        self.db_filepath = db_filepath
        self.table_name = table_name
        self.kwargs = kwargs
        
    def load(self, query: Optional[str] = None) -> pd.DataFrame:
        """
        Load data from SQL database.
        
        Args:
            query: Custom SQL query to execute. If None, selects all from table_name
            
        Returns:
            pd.DataFrame: Loaded data
        """
        if query is None:
            query = f"SELECT * FROM {self.table_name}"
            
        try:
            logging.info(f"Loading data from {self.db_filepath}, query: {query}")
            conn = sqlite3.connect(self.db_filepath)
            kwargs = {}
            kwargs.update(self.kwargs)
            data = pd.read_sql_query(query, conn, **kwargs)
            conn.close()
            return data
        except Exception as e:
            logging.error(f"Error loading data from SQL: {str(e)}")
            raise
            
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to SQL database.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
        """
        try:
            logging.info(f"Saving data to {self.db_filepath}, table: {self.table_name}")
            conn = sqlite3.connect(self.db_filepath)
            kwargs = {'if_exists': 'replace', 'index': False}
            kwargs.update(self.kwargs)
            data.to_sql(self.table_name, conn, **kwargs)
            conn.close()
            return True
        except Exception as e:
            logging.error(f"Error saving data to SQL: {str(e)}")
            raise


class JSONDataSource(DataSource):
    """Source for loading and saving JSON data."""
    
    def __init__(self, file_path: str, orient: str = 'records', **kwargs):
        """
        Initialize JSON data source.
        
        Args:
            file_path: Path to the JSON file
            orient: JSON orientation format
            **kwargs: Additional arguments to pass to pandas read_json/to_json
        """
        self.file_path = file_path
        self.orient = orient
        self.kwargs = kwargs
        
    def load(self) -> pd.DataFrame:
        """
        Load data from JSON file.
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            logging.info(f"Loading data from {self.file_path}")
            kwargs = {'orient': self.orient}
            kwargs.update(self.kwargs)
            data = pd.read_json(self.file_path, **kwargs)
            return data
        except Exception as e:
            logging.error(f"Error loading data from JSON: {str(e)}")
            raise
            
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to JSON.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
        """
        try:
            logging.info(f"Saving data to {self.file_path}")
            kwargs = {'orient': self.orient}
            kwargs.update(self.kwargs)
            data.to_json(self.file_path, **kwargs)
            return True
        except Exception as e:
            logging.error(f"Error saving data to JSON: {str(e)}")
            raise


class ExcelDataSource(DataSource):
    """Source for loading and saving Excel data."""
    
    def __init__(self, file_path: str, sheet_name: Union[str, int] = 0, **kwargs):
        """
        Initialize Excel data source.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Name or index of the sheet to load/save
            **kwargs: Additional arguments to pass to pandas read_excel/to_excel
        """
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.kwargs = kwargs
        
    def load(self) -> pd.DataFrame:
        """
        Load data from Excel file.
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            logging.info(f"Loading data from {self.file_path}, sheet: {self.sheet_name}")
            kwargs = {'sheet_name': self.sheet_name}
            kwargs.update(self.kwargs)
            data = pd.read_excel(self.file_path, **kwargs)
            return data
        except Exception as e:
            logging.error(f"Error loading data from Excel: {str(e)}")
            raise
            
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to Excel.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
        """
        try:
            logging.info(f"Saving data to {self.file_path}, sheet: {self.sheet_name}")
            kwargs = {'sheet_name': self.sheet_name, 'index': False}
            kwargs.update(self.kwargs)
            data.to_excel(self.file_path, **kwargs)
            return True
        except Exception as e:
            logging.error(f"Error saving data to Excel: {str(e)}")
            raise


class ParquetDataSource(DataSource):
    """Source for loading and saving Parquet data."""
    
    def __init__(self, file_path: str, **kwargs):
        """
        Initialize Parquet data source.
        
        Args:
            file_path: Path to the Parquet file
            **kwargs: Additional arguments to pass to pandas read_parquet/to_parquet
        """
        self.file_path = file_path
        self.kwargs = kwargs
        
    def load(self) -> pd.DataFrame:
        """
        Load data from Parquet file.
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            logging.info(f"Loading data from {self.file_path}")
            data = pd.read_parquet(self.file_path, **self.kwargs)
            return data
        except Exception as e:
            logging.error(f"Error loading data from Parquet: {str(e)}")
            raise
            
    def save(self, data: pd.DataFrame) -> bool:
        """
        Save DataFrame to Parquet.
        
        Args:
            data: DataFrame to save
            
        Returns:
            bool: True if save was successful
        """
        try:
            logging.info(f"Saving data to {self.file_path}")
            data.to_parquet(self.file_path, **self.kwargs)
            return True
        except Exception as e:
            logging.error(f"Error saving data to Parquet: {str(e)}")
            raise


if __name__ == '__main__':
    # Examples
    csv_source = CSVDataSource('data.csv')
    sql_source = SQLDataSource('db.sqlite')
    json_source = JSONDataSource('data.json')
    excel_source = ExcelDataSource('data.xlsx')

    # Create sample data
    data_to_write = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
    
    # Save to different formats
    csv_source.save(data_to_write)
    sql_source.save(data_to_write)
    json_source.save(data_to_write)
    excel_source.save(data_to_write)
    
    # Load from different formats
    csv_data = csv_source.load()
    sql_data = sql_source.load()
    json_data = json_source.load()
    excel_data = excel_source.load()
