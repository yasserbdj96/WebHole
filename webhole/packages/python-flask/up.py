def up(data,file_path, dest_path="./",other=None):
    import os
    import base64
    from pathlib import Path
    if other is not None and other!="None":
        os.chdir(dest_path)
        dest_path = other
    os.makedirs(dest_path, exist_ok=True)
    file_name = Path(str(file_path).replace("\\", "/")).name
    dest_file_path = os.path.join(dest_path, file_name)
    try:
        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        with open(dest_file_path, "wb") as f:
            f.write(base64.b64decode(data))
        return f"✅ File uploaded to {dest_file_path}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
    
print(up("__data__","__file__","__path__","__new_name__"))