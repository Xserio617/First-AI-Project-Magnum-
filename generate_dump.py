import os

# Output file name
OUTPUT_FILE = "project_dump.txt"

# Folders to completely ignore
IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".vscode",
    ".idea",
    "venv",
    "env",
    "node_modules",
    ".cache",
    "generated_images",
    "avatars",
    "assets" # Usually contains binary images
}

# Files to explicitly ignore
IGNORE_FILES = {
    "project_dump.txt",
    "generate_dump.py",
    "full_project_dump.py",
    ".DS_Store",
    "session.json", # Usually local session data, maybe exclude? I'll exclude it to be safe/clean
}

# Extensions to ignore (binaries, databases, etc.)
IGNORE_EXTENSIONS = {
    ".pyc",
    ".gguf",
    ".bin",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".exe",
    ".dll",
    ".so",
    ".o",
    ".ui" # PyQt UI files if they are binary, but usually XML. Check if user wants them. Assuming XML/Text is fine, but usually people use .py converted.
}

def is_text_file(filepath):
    """Simple check to see if a file is likely text."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            f.read(1024)
            return True
    except UnicodeDecodeError:
        return False
    except Exception:
        return False

def dump_project():
    print(f"Starting project dump to {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # Walk through the directory
        for root, dirs, files in os.walk("."):
            # Modify dirs in-place to exclude ignored directories
            # This prevents os.walk from entering these directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, ".").replace("\\", "/") # Normalize to forward slashes
                
                # Check explicit file ignores
                if file in IGNORE_FILES:
                    continue
                
                # Check extension ignores
                _, ext = os.path.splitext(file)
                if ext.lower() in IGNORE_EXTENSIONS:
                    continue
                
                # Check if file is text
                if not is_text_file(file_path):
                    print(f"Skipping binary file: {rel_path}")
                    continue
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    out.write(f"# ==========================================\n")
                    out.write(f"# FILE: {rel_path}\n")
                    out.write(f"# ==========================================\n")
                    out.write(content)
                    out.write("\n\n")
                    print(f"Included: {rel_path}")
                    
                except Exception as e:
                    print(f"Error reading {rel_path}: {e}")

    print(f"Dump complete! Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    dump_project()
