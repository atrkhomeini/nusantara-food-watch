import os
from pathlib import Path

def create_project_structure():
    # Definisi struktur folder dan file
    # Key = Nama Folder/File
    # Value = None (jika file) atau Dict (jika folder)
    structure = {
        "nusantara_food": {
            "dump": {
                "__init__.py": None
            },
            "data": {
                "raw": {},
                "interim": {},
                "processed": {}
            },
            "src": {
                "scraper": {
                    "debug": {
                        "debug_api.py": None,
                        "debug_monthly.py": None,
                        "find_endpoint.py": None
                    },
                    "pihps_scraper.py": None,
                    "app_scraper.py": None
                },
                "data_analysis": {
                    "cleaning.py": None,
                    "visualize.py": None,
                    "forecast.py": None,
                    "app_analysis.py": None
                },
                "models": {
                    "__init__.py": None
                },
                ".streamlit": {}, # Folder config streamlit
                "dashboard": {
                    "docs": {
                        "README": None
                    },
                    ".streamlit": {},
                    "app.py": None,
                    "setup.py": None,
                    "test.py": None,
                    "requirements.txt": None,
                    "Dockerfile": None,
                    "deploy_to_hf": {
                        ".streamlit": {},
                        "src": {
                            "__init__.py": None
                        },
                        "app.py": None,
                        "README": None,
                        "requirements.txt": None
                    }
                },
                "db": {
                    "test_db_setup.py": None,
                    "nusantara_db.py": None
                }
            },
            "notebooks": {
                "cleaning.ipynb": None,
                "visualize.ipynb": None,
                "forecast.ipynb": None
            },
            ".gitignore": None,
            "README": None,
            "requirements.txt": None,
            "main.py": None,
            ".env": None
        }
    }

    def build_tree(base_path, tree):
        for name, content in tree.items():
            path = base_path / name
            
            if content is None:
                # Ini adalah file
                if not path.exists():
                    path.touch()
                    print(f"[FILE] Created: {path}")
                    
                    # Optional: Isi .gitignore dengan template standar
                    if name == ".gitignore":
                        write_gitignore(path)
                else:
                    print(f"[SKIP] Exists: {path}")
            else:
                # Ini adalah folder
                path.mkdir(parents=True, exist_ok=True)
                print(f"[DIR]  Created: {path}")
                # Rekursif untuk isi folder
                build_tree(path, content)

    def write_gitignore(path):
        content = """
# Python
__pycache__/
*.py[cod]
*$py.class

# Environments
.env
.venv
env/
venv/
ENV/

# Data (Don't push huge data)
data/raw/*
data/interim/*
data/processed/*
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep

# IDE
.vscode/
.idea/

# Jupyter
.ipynb_checkpoints

# OS
.DS_Store
Thumbs.db
"""
        with open(path, "w") as f:
            f.write(content.strip())

    # Eksekusi pembuatan struktur dimulai dari direktori saat ini
    root_path = Path.cwd()
    print(f"Membangun struktur project di: {root_path}")
    build_tree(root_path, structure)
    print("\n✅ Selesai! Project 'nusantara_food' telah dibuat.")

if __name__ == "__main__":
    create_project_structure()