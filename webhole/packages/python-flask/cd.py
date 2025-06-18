def cd(path, old_path=None):
    import os
    if old_path is not None:
        try:
            os.chdir(old_path)
        except OSError:
            #print("❌ Error: Could not change to old path!")
            return old_path
    try:
        os.chdir(path)
        cwd = os.getcwd()
        # Normalize slashes and ensure proper Windows drive letter formatting
        cwd = os.path.normpath(cwd)
        if len(cwd) == 3 and cwd[1] == ":":
            cwd += "\\"  # Ensure "C:" becomes "C:\"
        return cwd
    except OSError:
        #print("❌ Error: Directory not found or permission denied!")
        return old_path
print(cd('__path__'))