def ls(path="."):
    import os
    import json
    try:
        path = os.path.normpath(os.path.abspath(path))

        # Ensure drive letters like "D:" are formatted as "D:\"
        if len(path) == 3 and path[1] == ":":
            path += r"\\"

        #path="D:\\"

        if not os.path.exists(path):
            return json.dumps([f"❌ Error: '{path}' not found."], ensure_ascii=False)

        items = os.listdir(path)
        result = [
            f"📁 {item}" if os.path.isdir(os.path.join(path, item)) else f"📄 {item}"
            for item in items
        ]
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps([f"❌ Error: {str(e)}"], ensure_ascii=False)
    
print(ls(r'__path__'))
