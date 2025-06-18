from typing import List
def get_dir_tree(dir_path: str = "./", relative_path: bool = True) -> List[str]:
    import os
    dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(dir_path):
        return [f"[✗] The Directory '{dir_path}' does not exist"]
    if not os.access(dir_path, os.R_OK):
        return [f"[✗] The Directory '{dir_path}' is not accessible"]
    
    lines = []
    root_name = os.path.basename(dir_path) if os.path.basename(dir_path) != '' else os.path.split(dir_path)[1]
    lines.append(f"{root_name}/")
    
    try:
        entries = list(os.scandir(dir_path))
    except Exception as e:
        return [f"[✗] Error accessing directory '{dir_path}': {str(e)}"]
    
    files = sorted([e for e in entries if e.is_file()], key=lambda x: x.name)
    dirs = sorted([e for e in entries if e.is_dir()], key=lambda x: x.name)
    combined = files + dirs
    
    def process_entries(entries, parent_prefix, is_last_parent, lines):
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└─── " if is_last else "├─── "
            line = f"{parent_prefix}{connector}{entry.name}"
            lines.append(line)
            if entry.is_dir():
                extension = "    " if is_last else "│   "
                new_prefix = parent_prefix + extension
                try:
                    sub_entries = list(os.scandir(entry.path))
                except Exception as e:
                    lines.append(f"{new_prefix}    [✗] Error accessing {entry.name}: {str(e)}")
                    continue
                sub_files = sorted([e for e in sub_entries if e.is_file()], key=lambda x: x.name)
                sub_dirs = sorted([e for e in sub_entries if e.is_dir()], key=lambda x: x.name)
                sub_combined = sub_files + sub_dirs
                process_entries(sub_combined, new_prefix, is_last, lines)
    
    process_entries(combined, "", False, lines)
    
    # Adjusting the root line to match the example's "D:." style
    if lines:
        lines[0] = "."
    return lines

# Example usage
if __name__ == "__main__":
    tree = get_dir_tree('__path__')
    for value in tree:
        print(value)