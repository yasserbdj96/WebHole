def cat(path, old_path=None):
    import os
    os.chdir(old_path)
    """Reads and prints the content of a file."""
    if not os.path.isfile(path):
        return f"Error: '{path}' is not a valid file."
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

print(cat("__path__"))