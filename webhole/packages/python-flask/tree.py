from typing import List
def get_dir_tree(dir_path: str = "./") -> List[str]:
    import os
    dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(dir_path):
        return [f"[✗] The directory '{dir_path}' does not exist"]
    if not os.access(dir_path, os.R_OK):
        return [f"[✗] The directory '{dir_path}' is not accessible"]

    lines: List[str] = []

    def scan(path: str, prefix: str = ""):
        try:
            entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
        except Exception as e:
            lines.append(f"{prefix}[✗] Error accessing '{path}': {e}")
            return

        for i, entry in enumerate(entries):
            connector = "└─── " if i == len(entries) - 1 else "├─── "
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                scan(entry.path, prefix + extension)

    lines.append(".")
    scan(dir_path)
    return lines


# Example usage
if __name__ == "__main__":
    tree = get_dir_tree('__path__')
    for value in tree:
        print(value)