from typing import List
def get_dir_contents(dir_path: str = "./", relative_path: bool = True) -> List[str]:
    import os
    import stat
    import time
    dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(dir_path):
        return [f"[✗] The Directory '{dir_path}' does not exist"]
    if not os.access(dir_path, os.R_OK):
        return [f"[✗] The Directory '{dir_path}' is not accessible"]

    file_list = []
    
    try:
        for root, _, files in os.walk(dir_path, topdown=True, followlinks=False):
            for filename in files:
                full_path = os.path.join(root, filename)
                try:
                    st = os.lstat(full_path)
                except Exception:
                    continue
                
                if stat.S_ISDIR(st.st_mode):
                    continue
                
                # Determine file type
                file_type = 'u'
                mode = st.st_mode
                if stat.S_ISSOCK(mode):
                    file_type = 's'
                elif stat.S_ISLNK(mode):
                    file_type = 'l'
                elif stat.S_ISREG(mode):
                    file_type = 'r'
                elif stat.S_ISBLK(mode):
                    file_type = 'b'
                elif stat.S_ISCHR(mode):
                    file_type = 'c'
                elif stat.S_ISFIFO(mode):
                    file_type = 'p'
                
                # Build permissions string
                permissions = []
                # User permissions
                permissions.append('r' if mode & stat.S_IRUSR else '-')
                permissions.append('w' if mode & stat.S_IWUSR else '-')
                if mode & stat.S_IXUSR:
                    permissions.append('s' if mode & stat.S_ISUID else 'x')
                else:
                    permissions.append('S' if mode & stat.S_ISUID else '-')
                
                # Group permissions
                permissions.append('r' if mode & stat.S_IRGRP else '-')
                permissions.append('w' if mode & stat.S_IWGRP else '-')
                if mode & stat.S_IXGRP:
                    permissions.append('s' if mode & stat.S_ISGID else 'x')
                else:
                    permissions.append('S' if mode & stat.S_ISGID else '-')
                
                # Others permissions
                permissions.append('r' if mode & stat.S_IROTH else '-')
                permissions.append('w' if mode & stat.S_IWOTH else '-')
                if mode & stat.S_IXOTH:
                    permissions.append('t' if mode & stat.S_ISVTX else 'x')
                else:
                    permissions.append('T' if mode & stat.S_ISVTX else '-')
                
                perm_str = file_type + ''.join(permissions)
                
                # Last modified time
                last_modified = time.strftime('%b %d %H:%M', time.localtime(st.st_mtime))
                
                # File size formatting
                bytes = st.st_size
                if bytes >= 1073741824:
                    size_str = f"{bytes / 1073741824:.2f} GB"
                elif bytes >= 1048576:
                    size_str = f"{bytes / 1048576:.2f} MB"
                elif bytes >= 1024:
                    size_str = f"{bytes / 1024:.2f} KB"
                else:
                    size_str = f"{bytes} byte{'s' if bytes != 1 else ''}"
                size_str = size_str.rjust(11)
                
                # Handle relative path
                rel_path = os.path.relpath(full_path, dir_path).replace(os.path.sep, '/')
                
                file_list.append(f"{perm_str} {last_modified} {size_str} {rel_path}")
    
    except Exception as e:
        return [f"[✗] Error accessing directory '{dir_path}': {str(e)}"]
    
    return file_list

# Example usage
import json
print(json.dumps(get_dir_contents('__path__'), indent=2))