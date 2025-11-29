"""
Configuration for Data Analysis Pipeline
Centralized paths and settings for Nusantara Food Watch notebooks

Usage in notebooks:
    from src.data_analysis.config import INTERIM_DIR, PROCESSED_DIR, FIGURES_DIR
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# PROJECT PATHS (auto-detect from this file's location)
# ============================================================================

# This file is at: src/data_analysis/config.py
# Project root is: ../../ from here
PROJECT_ROOT = Path(__file__).parent.parent.parent

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DATABASE_URL = os.getenv('DATABASE_URL')

# ============================================================================
# DATA DIRECTORIES
# ============================================================================

DATA_DIR = PROJECT_ROOT / 'data'
RAW_DIR = DATA_DIR / 'raw'              # Original scraped data (backup)
INTERIM_DIR = DATA_DIR / 'interim'      # Intermediate analysis outputs
PROCESSED_DIR = DATA_DIR / 'processed'  # Final cleaned datasets

# ============================================================================
# REPORTS & OUTPUT
# ============================================================================

REPORTS_DIR = PROJECT_ROOT / 'reports'
FIGURES_DIR = REPORTS_DIR / 'figures'   # Generated charts/images

# ============================================================================
# NOTEBOOKS
# ============================================================================

NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'

# ============================================================================
# AUTO-CREATE DIRECTORIES
# ============================================================================

# Create directories if they don't exist
for directory in [RAW_DIR, INTERIM_DIR, PROCESSED_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# FILE NAMING HELPERS
# ============================================================================

def get_interim_path(filename: str) -> Path:
    """
    Get full path for interim data file
    
    Args:
        filename: Name of file (e.g., 'prices_extract.csv')
    
    Returns:
        Full path to data/interim/{filename}
    
    Example:
        >>> path = get_interim_path('beras_2024.csv')
        >>> print(path)
        D:\\nusantara_food\\data\\interim\\beras_2024.csv
    """
    return INTERIM_DIR / filename


def get_processed_path(filename: str) -> Path:
    """
    Get full path for processed data file
    
    Args:
        filename: Name of file (e.g., 'prices_cleaned.csv')
    
    Returns:
        Full path to data/processed/{filename}
    
    Example:
        >>> path = get_processed_path('prices_final.csv')
        >>> print(path)
        D:\\nusantara_food\\data\\processed\\prices_final.csv
    """
    return PROCESSED_DIR / filename


def get_figure_path(filename: str) -> Path:
    """
    Get full path for figure file
    
    Args:
        filename: Name of file (e.g., 'price_trend.png')
    
    Returns:
        Full path to reports/figures/{filename}
    
    Example:
        >>> path = get_figure_path('chart.png')
        >>> print(path)
        D:\\nusantara_food\\reports\\figures\\chart.png
    """
    return FIGURES_DIR / filename


# ============================================================================
# ANALYSIS SETTINGS
# ============================================================================

# Default commodities to analyze
DEFAULT_COMMODITIES = [
    'cat_1',   # Beras
    'cat_2',   # Daging Ayam
    'cat_4',   # Telur Ayam
    'cat_5',   # Bawang Merah
    'cat_9',   # Minyak Goreng
    'cat_10'   # Gula Pasir
]

# Market types
MARKET_TYPES = {
    1: 'Pasar Tradisional',
    2: 'Pasar Modern',
    3: 'Pedagang Besar',
    4: 'Produsen'
}

# Plot settings
PLOT_STYLE = 'whitegrid'
PLOT_PALETTE = 'husl'
DEFAULT_FIGURE_SIZE = (12, 6)
DEFAULT_DPI = 300

# Date format for filenames
DATE_FORMAT = '%Y%m%d'
DATETIME_FORMAT = '%Y%m%d_%H%M%S'

# ============================================================================
# UTILITY: Print configuration (for debugging)
# ============================================================================

def print_config():
    """Print current configuration for debugging"""
    
    print("=" * 70)
    print("📊 NUSANTARA FOOD WATCH - DATA ANALYSIS CONFIGURATION")
    print("=" * 70)
    
    print(f"\n📁 Project Paths:")
    print(f"   Root: {PROJECT_ROOT}")
    print(f"   Data: {DATA_DIR}")
    print(f"   Interim: {INTERIM_DIR}")
    print(f"   Processed: {PROCESSED_DIR}")
    print(f"   Figures: {FIGURES_DIR}")
    print(f"   Notebooks: {NOTEBOOKS_DIR}")
    
    print(f"\n🗄️  Database:")
    print(f"   URL: {DATABASE_URL[:30]}..." if DATABASE_URL else "   URL: Not configured")
    
    print(f"\n🎨 Plot Settings:")
    print(f"   Style: {PLOT_STYLE}")
    print(f"   Palette: {PLOT_PALETTE}")
    print(f"   Figure Size: {DEFAULT_FIGURE_SIZE}")
    print(f"   DPI: {DEFAULT_DPI}")
    
    print(f"\n🛒 Default Commodities:")
    for cat in DEFAULT_COMMODITIES:
        print(f"   • {cat}")
    
    print("\n" + "=" * 70)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Print configuration
    print_config()
    
    # Test path helpers
    print("\n🧪 Testing path helpers:")
    print(f"   Interim: {get_interim_path('test.csv')}")
    print(f"   Processed: {get_processed_path('test.csv')}")
    print(f"   Figure: {get_figure_path('test.png')}")
    
    # Check if directories exist
    print("\n✅ Directory check:")
    for name, path in [
        ('Interim', INTERIM_DIR),
        ('Processed', PROCESSED_DIR),
        ('Figures', FIGURES_DIR)
    ]:
        exists = "✅" if path.exists() else "❌"
        print(f"   {exists} {name}: {path}")
