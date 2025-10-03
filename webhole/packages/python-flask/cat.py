def cat(path, old_path=None):
    import os

    if old_path:
        os.chdir(old_path)

    """Reads and returns the content of a file (text or binary)."""
    if not os.path.isfile(path):
        return f"Error: '{path}' is not a valid file."

    try:
        # Try reading as text (UTF-8)
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except (UnicodeDecodeError, Exception):
        # Return raw binary data directly (not repr)
        with open(path, 'rb') as file:
            return file.read()



print(cat("__path__"))