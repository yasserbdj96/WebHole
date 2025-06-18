<?php
function getDirContents($dir = "./", $relativePath = false) {
    if (!is_dir($dir)) {
        return ["[✗] The Directory '{$dir}' does not exist"];
    }

    $fileList = array();
    
    try {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS)
        );
    } catch (Exception $e) {
        return ["[✗] Error: " . $e->getMessage()];
    }

    foreach ($iterator as $file) {
        if ($file->isDir()) continue;
        
        $path = $file->getPathname();
        
        // Skip files that cannot be accessed
        if (!is_readable($path)) continue;

        if ($relativePath) {
            $path = str_replace($dir, '', $path);
            $path = ltrim($path, '/');
        }

        $perms = @fileperms($path);
        if ($perms === false) continue; // Skip if permissions cannot be read

        // File permission info
        switch ($perms & 0xF000) {
            case 0xC000: $info = 's'; break;
            case 0xA000: $info = 'l'; break;
            case 0x8000: $info = 'r'; break;
            case 0x6000: $info = 'b'; break;
            case 0x4000: $info = 'd'; break;
            case 0x2000: $info = 'c'; break;
            case 0x1000: $info = 'p'; break;
            default: $info = 'u';
        }

        // Owner permissions
        $info .= (($perms & 0x0100) ? 'r' : '-');
        $info .= (($perms & 0x0080) ? 'w' : '-');
        $info .= (($perms & 0x0040) ? (($perms & 0x0800) ? 's' : 'x') : (($perms & 0x0800) ? 'S' : '-'));

        // Group permissions
        $info .= (($perms & 0x0020) ? 'r' : '-');
        $info .= (($perms & 0x0010) ? 'w' : '-');
        $info .= (($perms & 0x0008) ? (($perms & 0x0400) ? 's' : 'x') : (($perms & 0x0400) ? 'S' : '-'));

        // World permissions
        $info .= (($perms & 0x0004) ? 'r' : '-');
        $info .= (($perms & 0x0002) ? 'w' : '-');
        $info .= (($perms & 0x0001) ? (($perms & 0x0200) ? 't' : 'x') : (($perms & 0x0200) ? 'T' : '-'));

        // File statistics
        $file_stats = @stat($path);
        if ($file_stats === false) continue; // Skip if file stats cannot be read

        $last_use = date('M d H:i', $file_stats["mtime"]);

        // Format file size
        $bytes = @filesize($path);
        if ($bytes === false) continue; // Skip if file size cannot be read

        if ($bytes >= 1073741824) {
            $bytes = number_format($bytes / 1073741824, 2) . ' GB';
        } elseif ($bytes >= 1048576) {
            $bytes = number_format($bytes / 1048576, 2) . ' MB';
        } elseif ($bytes >= 1024) {
            $bytes = number_format($bytes / 1024, 2) . ' KB';
        } else {
            $bytes = $bytes . ' bytes';
        }

        $fileList[] = $info . " " . $last_use . " " . str_pad($bytes, 11, " ", STR_PAD_LEFT) . " " . $path;
    }

    return $fileList;
}

echo json_encode(getDirContents('__path__'));