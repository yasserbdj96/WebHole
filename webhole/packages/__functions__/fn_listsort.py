def fn_listsort(response, separator='    |    '):
    import ast
    import os
    import shutil
    try:
        response = response.strip()  # Remove leading/trailing spaces/newlines
        if not response.startswith("[") or not response.endswith("]"):
            print(f"❌ Invalid response: {response}")  # Debugging line
            raise ValueError(f"❌ Invalid response format: {response}")

        lslist = ast.literal_eval(response)
        
        if not isinstance(lslist, list):
            raise ValueError("❌ Parsed response is not a list.")
        
        lslist = [os.path.normpath(item) for item in lslist]  # Normalize paths

        # Get terminal size safely
        try:
            ts = shutil.get_terminal_size(fallback=(120, 50))
        except:
            ts = os.get_terminal_size(0)

        # Calculate column width based on longest item
        max_length = len(max(lslist, key=len, default=""))
        num_columns = max(1, ts.columns // (max_length + len(separator)))  # Avoid zero division
        
        # Format output
        formatted_list = ""
        for idx, key in enumerate(lslist):
            if (idx + 1) % num_columns:
                formatted_list += key.ljust(max_length) + separator
            else:
                formatted_list += key + '\n'
        
        return formatted_list.strip()
    
    except (SyntaxError, ValueError) as e:
        return f"❌ Error: Unable to parse response - {str(e)}{response}"
