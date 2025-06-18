<?php
function cat($path, $old_path = null) {
    if ($old_path !== null) {
        chdir($old_path);
    }

    // Check if the file exists and is a regular file
    if (!is_file($path)) {
        return "Error: '$path' is not a valid file.";
    }

    // Attempt to read the file
    try {
        return file_get_contents($path);
    } catch (Exception $e) {
        return "Error reading file: " . $e->getMessage();
    }
}

echo cat("__path__");