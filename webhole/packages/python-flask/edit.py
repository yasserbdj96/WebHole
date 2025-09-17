def edit(path_to_edit, new_b64_text):
    try:
        import os, base64
        # Normalize the path (removes accidental \n, \r, etc.)
        path_to_edit = os.path.normpath(path_to_edit.strip())
        print(path_to_edit)
        # Ensure directory exists
        dir_name = os.path.dirname(path_to_edit)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, mode=0o777, exist_ok=True)
        # Write file
        if new_b64_text=="" or new_b64_text==None:
            print(f"⚠️ Warning: No content was saved. The file editor for '{path_to_edit}' was closed or left empty.")
        else:
            with open(path_to_edit, "wb") as f:  # overwrite mode
                    f.write(base64.b64decode(new_b64_text))
                    print(f"✅ File '{path_to_edit}' edited successfully.")
    except Exception as e:
        print(f"❌ Error editing file '{path_to_edit}': {str(e)}")

edit("__path__", "__new_b64_text__")