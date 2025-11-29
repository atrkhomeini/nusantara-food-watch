"""
Setup Data Analysis Environment
Creates all necessary folders and files for Nusantara Food Watch analysis

Run this from project root: D:\nusantara_food
"""

import os
from pathlib import Path

def setup_analysis_folders():
    """Create all required folders for data analysis"""
    
    folders = [
        'data/raw',
        'data/interim',
        'data/processed',
        'reports/figures',
        'notebooks',
        'src/data_analysis'
    ]
    
    print("=" * 70)
    print("📁 SETTING UP DATA ANALYSIS ENVIRONMENT")
    print("=" * 70)
    
    created = 0
    existed = 0
    
    for folder in folders:
        folder_path = Path(folder)
        
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {folder}")
            created += 1
        else:
            print(f"  ⏭️  Exists: {folder}")
            existed += 1
    
    return created, existed


def create_gitkeep_files():
    """Create .gitkeep in data directories to preserve folder structure in git"""
    
    print("\n" + "=" * 70)
    print("📝 CREATING .gitkeep FILES")
    print("=" * 70)
    
    gitkeep_dirs = [
        'data/raw',
        'data/interim', 
        'data/processed',
        'reports/figures'
    ]
    
    created = 0
    
    for directory in gitkeep_dirs:
        gitkeep_path = Path(directory) / '.gitkeep'
        
        if not gitkeep_path.exists():
            gitkeep_path.write_text('# Keep this directory in git\n')
            print(f"  ✅ Created: {gitkeep_path}")
            created += 1
        else:
            print(f"  ⏭️  Exists: {gitkeep_path}")
    
    return created


def create_init_files():
    """Create __init__.py in src/data_analysis"""
    
    print("\n" + "=" * 70)
    print("📦 CREATING PACKAGE FILES")
    print("=" * 70)
    
    init_file = Path('src/data_analysis/__init__.py')
    
    if not init_file.exists():
        init_file.write_text('"""Data Analysis package for Nusantara Food Watch"""\n')
        print(f"  ✅ Created: {init_file}")
        return 1
    else:
        print(f"  ⏭️  Exists: {init_file}")
        return 0


def create_readme_files():
    """Create README files in data directories"""
    
    print("\n" + "=" * 70)
    print("📄 CREATING README FILES")
    print("=" * 70)
    
    readmes = {
        'data/interim/README.md': """# Interim Data

This folder contains intermediate analysis outputs.

**Purpose:** Work-in-progress data files that are outputs from extraction notebooks but not yet final.

**Examples:**
- `all_prices_raw.csv` - Raw extracted data from database
- `beras_prices_2024.csv` - Filtered commodity data
- `supply_chain_extract.csv` - Supply chain data before cleaning

**Lifecycle:** These files can be regenerated and are temporary.
""",
        'data/processed/README.md': """# Processed Data

This folder contains final, analysis-ready datasets.

**Purpose:** Cleaned, transformed, and validated data ready for visualization and modeling.

**Examples:**
- `prices_cleaned_2024.csv` - Cleaned price data
- `food_basket_final.csv` - Final food basket calculations
- `inflation_metrics_monthly.csv` - Computed inflation metrics

**Lifecycle:** These are final outputs that feed into reports and dashboards.
""",
        'reports/figures/README.md': """# Figures

This folder contains all generated charts and visualizations.

**Purpose:** Publication-ready figures for reports and presentations.

**Naming Convention:** `{topic}_{type}_{date}.png`

**Examples:**
- `beras_price_trend_2024.png`
- `supply_chain_margins_comparison.png`
- `provincial_disparity_heatmap_nov2024.png`

**Format:** PNG at 300 DPI for print quality.
"""
    }
    
    created = 0
    
    for filepath, content in readmes.items():
        readme_path = Path(filepath)
        
        if not readme_path.exists():
            readme_path.write_text(content)
            print(f"  ✅ Created: {readme_path}")
            created += 1
        else:
            print(f"  ⏭️  Exists: {readme_path}")
    
    return created


def print_summary(folders_created, gitkeep_created, init_created, readme_created):
    """Print setup summary"""
    
    print("\n" + "=" * 70)
    print("📊 SETUP SUMMARY")
    print("=" * 70)
    print(f"  ✅ Folders created: {folders_created}")
    print(f"  ✅ .gitkeep files: {gitkeep_created}")
    print(f"  ✅ __init__.py files: {init_created}")
    print(f"  ✅ README files: {readme_created}")
    
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    
    print("\n📁 Your folder structure:")
    print("""
    nusantara_food/
    ├── data/
    │   ├── raw/           ✅ (backup original data)
    │   ├── interim/       ✅ (work in progress)
    │   └── processed/     ✅ (analysis ready)
    ├── reports/
    │   └── figures/       ✅ (charts & images)
    └── src/
        └── data_analysis/ ✅ (utilities)
    """)
    
    print("\n🎯 Next steps:")
    print("  1. Create config.py and utils.py in src/data_analysis/")
    print("  2. Start with notebooks/01_data_extraction.ipynb")
    print("  3. Follow the workflow in DATA_ANALYSIS_SETUP.md")


def verify_structure():
    """Verify that everything is set up correctly"""
    
    print("\n" + "=" * 70)
    print("🔍 VERIFYING STRUCTURE")
    print("=" * 70)
    
    required = [
        'data/interim',
        'data/processed',
        'reports/figures',
        'notebooks',
        'src/data_analysis'
    ]
    
    all_ok = True
    
    for directory in required:
        if Path(directory).exists():
            print(f"  ✅ {directory}")
        else:
            print(f"  ❌ MISSING: {directory}")
            all_ok = False
    
    return all_ok


def main():
    """Main setup execution"""
    
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 12 + "NUSANTARA FOOD WATCH - DATA ANALYSIS SETUP" + " " * 14 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Check current directory
    cwd = Path.cwd()
    print(f"\n📍 Current directory: {cwd}")
    
    if 'nusantara_food' not in str(cwd).lower():
        print("\n⚠️  WARNING: You might not be in the project directory")
        response = input("\nContinue anyway? (y/n): ").lower()
        if response != 'y':
            print("\n⏸️  Setup cancelled")
            return
    
    # Run setup
    folders_created, folders_existed = setup_analysis_folders()
    gitkeep_created = create_gitkeep_files()
    init_created = create_init_files()
    readme_created = create_readme_files()
    
    # Summary
    print_summary(folders_created, gitkeep_created, init_created, readme_created)
    
    # Verify
    if verify_structure():
        print("\n✅ All required directories present!")
    else:
        print("\n⚠️  Some directories are missing. Please check above.")
    
    print("\n" + "=" * 70)
    print("✨ Ready to start data analysis!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
