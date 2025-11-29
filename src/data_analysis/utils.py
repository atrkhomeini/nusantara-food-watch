"""
Utility Functions for Data Analysis
Common operations used across Nusantara Food Watch notebooks

Usage in notebooks:
    from src.data_analysis.utils import DataLoader, DataSaver, load_data, save_csv
"""

import pandas as pd
import psycopg2
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional, Dict, List, Tuple

load_dotenv()

# Import config
try:
    from .config import (
        DATABASE_URL, 
        get_interim_path, 
        get_processed_path, 
        get_figure_path,
        PLOT_STYLE,
        PLOT_PALETTE,
        DEFAULT_FIGURE_SIZE,
        DEFAULT_DPI
    )
except ImportError:
    # Fallback for direct execution
    from config import (
        DATABASE_URL, 
        get_interim_path, 
        get_processed_path, 
        get_figure_path,
        PLOT_STYLE,
        PLOT_PALETTE,
        DEFAULT_FIGURE_SIZE,
        DEFAULT_DPI
    )


# ============================================================================
# DATA LOADING CLASS
# ============================================================================

class DataLoader:
    """
    Helper class for loading data from database
    
    Examples:
        >>> loader = DataLoader()
        >>> df = loader.query_to_df("SELECT * FROM harga_pangan LIMIT 100")
        >>> loader.close()
        
        # Or use context manager
        >>> with DataLoader() as loader:
        ...     df = loader.get_latest_prices()
    """
    
    def __init__(self, database_url: str = None):
        """
        Initialize data loader
        
        Args:
            database_url: PostgreSQL connection string (defaults to env var)
        """
        self.database_url = database_url or DATABASE_URL
        self.conn = None
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def connect(self):
        """Connect to database"""
        if not self.conn:
            self.conn = psycopg2.connect(self.database_url)
        return self.conn
    
    def query_to_df(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return DataFrame
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with query results
        
        Example:
            >>> df = loader.query_to_df('''
            ...     SELECT provinsi, tanggal, harga
            ...     FROM harga_pangan
            ...     WHERE commodity_category = 'cat_1'
            ...     LIMIT 1000
            ... ''')
        """
        if not self.conn:
            self.connect()
        return pd.read_sql(query, self.conn)
    
    def get_latest_prices(
        self, 
        commodity: Optional[str] = None, 
        province: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get latest prices with optional filters
        
        Args:
            commodity: Filter by commodity_category (e.g., 'cat_1')
            province: Filter by province name (e.g., 'DKI Jakarta')
            
        Returns:
            DataFrame with latest prices
            
        Example:
            >>> df = loader.get_latest_prices(commodity='cat_1')
            >>> df = loader.get_latest_prices(province='DKI Jakarta')
        """
        query = "SELECT * FROM latest_prices WHERE 1=1"
        
        if commodity:
            query += f" AND commodity_category = '{commodity}'"
        if province:
            query += f" AND provinsi = '{province}'"
        
        return self.query_to_df(query)
    
    def get_price_history(
        self, 
        commodity: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        market_type: Optional[int] = None,
        province: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get price history for a commodity
        
        Args:
            commodity: Commodity category (e.g., 'cat_1')
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            market_type: Market type ID (1-4)
            province: Province name
            
        Returns:
            DataFrame with price history
            
        Example:
            >>> df = loader.get_price_history(
            ...     commodity='cat_1',
            ...     start_date='2024-01-01',
            ...     market_type=1
            ... )
        """
        query = f"""
        SELECT 
            provinsi,
            tanggal,
            harga,
            commodity_name,
            market_type_name,
            report_type
        FROM harga_pangan
        WHERE commodity_category = '{commodity}'
        """
        
        if start_date:
            query += f" AND tanggal >= '{start_date}'"
        if end_date:
            query += f" AND tanggal <= '{end_date}'"
        if market_type:
            query += f" AND market_type_id = {market_type}"
        if province:
            query += f" AND provinsi = '{province}'"
        
        query += " ORDER BY tanggal, provinsi"
        
        return self.query_to_df(query)
    
    def get_supply_chain_margins(
        self,
        commodity: Optional[str] = None,
        province: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get supply chain margin analysis
        
        Args:
            commodity: Commodity category (e.g., 'cat_1')
            province: Province name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with margin calculations
            
        Example:
            >>> df = loader.get_supply_chain_margins(
            ...     commodity='cat_1',
            ...     province='DKI Jakarta'
            ... )
        """
        query = "SELECT * FROM supply_chain_margins WHERE 1=1"
        
        if commodity:
            query += f" AND commodity_category = '{commodity}'"
        if province:
            query += f" AND provinsi = '{province}'"
        if start_date:
            query += f" AND tanggal >= '{start_date}'"
        if end_date:
            query += f" AND tanggal <= '{end_date}'"
        
        query += " ORDER BY tanggal DESC"
        
        return self.query_to_df(query)
    
    def get_summary_stats(self) -> Dict:
        """
        Get database summary statistics
        
        Returns:
            Dictionary with summary stats
            
        Example:
            >>> stats = loader.get_summary_stats()
            >>> print(f"Total records: {stats['total_records']}")
        """
        query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT provinsi) as total_provinces,
            COUNT(DISTINCT commodity_category) as total_commodities,
            MIN(tanggal) as earliest_date,
            MAX(tanggal) as latest_date,
            AVG(harga) as avg_price,
            MIN(harga) as min_price,
            MAX(harga) as max_price
        FROM harga_pangan
        """
        
        df = self.query_to_df(query)
        return df.iloc[0].to_dict()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


# ============================================================================
# DATA SAVING CLASS
# ============================================================================

class DataSaver:
    """
    Helper class for saving analysis outputs
    
    Examples:
        >>> saver = DataSaver()
        >>> saver.save_interim(df, 'my_data.csv')
        >>> saver.save_processed(df_clean, 'final_data.csv')
        >>> saver.save_figure(fig, 'chart.png')
    """
    
    @staticmethod
    def save_interim(
        df: pd.DataFrame, 
        filename: str, 
        add_timestamp: bool = False,
        **kwargs
    ) -> Path:
        """
        Save DataFrame to data/interim
        
        Args:
            df: DataFrame to save
            filename: Output filename (e.g., 'my_data.csv')
            add_timestamp: Add timestamp to filename
            **kwargs: Additional arguments for to_csv()
            
        Returns:
            Path to saved file
            
        Example:
            >>> path = saver.save_interim(df, 'prices_extract.csv')
            💾 Saved interim data: D:\\nusantara_food\\data\\interim\\prices_extract.csv
        """
        if add_timestamp:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{timestamp}.{ext}"
        
        filepath = get_interim_path(filename)
        
        # Default to not include index unless specified
        if 'index' not in kwargs:
            kwargs['index'] = False
        
        df.to_csv(filepath, **kwargs)
        print(f"💾 Saved interim data: {filepath}")
        return filepath
    
    @staticmethod
    def save_processed(
        df: pd.DataFrame, 
        filename: str, 
        add_timestamp: bool = False,
        **kwargs
    ) -> Path:
        """
        Save DataFrame to data/processed
        
        Args:
            df: DataFrame to save
            filename: Output filename (e.g., 'final_data.csv')
            add_timestamp: Add timestamp to filename
            **kwargs: Additional arguments for to_csv()
            
        Returns:
            Path to saved file
            
        Example:
            >>> path = saver.save_processed(df, 'prices_cleaned.csv')
            💾 Saved processed data: D:\\nusantara_food\\data\\processed\\prices_cleaned.csv
        """
        if add_timestamp:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{timestamp}.{ext}"
        
        filepath = get_processed_path(filename)
        
        # Default to not include index unless specified
        if 'index' not in kwargs:
            kwargs['index'] = False
        
        df.to_csv(filepath, **kwargs)
        print(f"💾 Saved processed data: {filepath}")
        return filepath
    
    @staticmethod
    def save_figure(
        fig, 
        filename: str, 
        dpi: int = DEFAULT_DPI, 
        bbox_inches: str = 'tight',
        add_timestamp: bool = False,
        **kwargs
    ) -> Path:
        """
        Save matplotlib/seaborn figure to reports/figures
        
        Args:
            fig: Matplotlib figure object
            filename: Output filename (e.g., 'chart.png')
            dpi: Resolution (default 300)
            bbox_inches: Bounding box (default 'tight')
            add_timestamp: Add timestamp to filename
            **kwargs: Additional arguments for savefig()
            
        Returns:
            Path to saved file
            
        Example:
            >>> fig, ax = plt.subplots()
            >>> ax.plot([1, 2, 3], [1, 2, 3])
            >>> path = saver.save_figure(fig, 'line_chart.png')
            🎨 Saved figure: D:\\nusantara_food\\reports\\figures\\line_chart.png
        """
        if add_timestamp:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name, ext = filename.rsplit('.', 1)
            filename = f"{name}_{timestamp}.{ext}"
        
        filepath = get_figure_path(filename)
        fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches, **kwargs)
        print(f"🎨 Saved figure: {filepath}")
        return filepath


# ============================================================================
# PLOTTING UTILITIES
# ============================================================================

def setup_plot_style():
    """
    Setup consistent plotting style for all notebooks
    
    Example:
        >>> setup_plot_style()
        >>> fig, ax = plt.subplots()  # Uses configured style
    """
    sns.set_style(PLOT_STYLE)
    sns.set_palette(PLOT_PALETTE)
    
    plt.rcParams['figure.figsize'] = DEFAULT_FIGURE_SIZE
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 16


# ============================================================================
# QUICK ACCESS FUNCTIONS
# ============================================================================

def load_data(query: str) -> pd.DataFrame:
    """
    Quick function to load data from database
    
    Automatically handles connection and cleanup.
    
    Args:
        query: SQL query string
        
    Returns:
        DataFrame with query results
        
    Example:
        >>> df = load_data("SELECT * FROM harga_pangan LIMIT 100")
    """
    with DataLoader() as loader:
        return loader.query_to_df(query)


def save_csv(
    df: pd.DataFrame, 
    filename: str, 
    processed: bool = False,
    **kwargs
) -> Path:
    """
    Quick function to save CSV
    
    Args:
        df: DataFrame to save
        filename: Output filename
        processed: If True, save to data/processed; if False, save to data/interim
        **kwargs: Additional arguments for to_csv()
        
    Returns:
        Path to saved file
        
    Example:
        >>> save_csv(df, 'my_data.csv', processed=False)  # Saves to interim
        >>> save_csv(df_clean, 'final.csv', processed=True)  # Saves to processed
    """
    saver = DataSaver()
    if processed:
        return saver.save_processed(df, filename, **kwargs)
    else:
        return saver.save_interim(df, filename, **kwargs)


# ============================================================================
# DATA QUALITY HELPERS
# ============================================================================

def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get summary of missing values
    
    Args:
        df: DataFrame to check
        
    Returns:
        DataFrame with missing value counts and percentages
        
    Example:
        >>> missing = check_missing_values(df)
        >>> print(missing)
    """
    missing = df.isnull().sum()
    percent = (missing / len(df)) * 100
    
    result = pd.DataFrame({
        'Missing Count': missing,
        'Percentage': percent
    })
    
    return result[result['Missing Count'] > 0].sort_values('Missing Count', ascending=False)


def detect_outliers_iqr(
    df: pd.DataFrame, 
    column: str, 
    multiplier: float = 1.5
) -> Tuple[pd.Series, float, float]:
    """
    Detect outliers using IQR method
    
    Args:
        df: DataFrame
        column: Column name to check
        multiplier: IQR multiplier (default 1.5)
        
    Returns:
        Tuple of (outlier_mask, lower_bound, upper_bound)
        
    Example:
        >>> outliers, lower, upper = detect_outliers_iqr(df, 'harga')
        >>> print(f"Outliers: {outliers.sum()}")
        >>> df_clean = df[~outliers]
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    outlier_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
    
    return outlier_mask, lower_bound, upper_bound


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTING DATA ANALYSIS UTILITIES")
    print("=" * 70)
    
    # Test 1: Load data
    print("\n1️⃣ Testing data loading...")
    try:
        df = load_data("SELECT * FROM harga_pangan LIMIT 10")
        print(f"   ✅ Loaded {len(df)} records")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Save CSV
    print("\n2️⃣ Testing CSV saving...")
    try:
        test_df = pd.DataFrame({'test': [1, 2, 3]})
        path = save_csv(test_df, 'test_file.csv', processed=False)
        print(f"   ✅ Saved to: {path}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Plot style
    print("\n3️⃣ Testing plot setup...")
    try:
        setup_plot_style()
        print(f"   ✅ Plot style configured")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Testing complete!")
    print("=" * 70)
