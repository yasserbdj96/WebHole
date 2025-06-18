<?php
function cd($path, $old_path = null) {
    if ($old_path !== null) {
        if (!@chdir($old_path)) {
            return "Error: Could not change to old path!";
        }
    }

    if (@chdir($path)) {
        $cwd = getcwd();

        // Normalize slashes and ensure the path is properly formatted
        $cwd = preg_replace('/[\/\\\\]+/', DIRECTORY_SEPARATOR, $cwd);

        // Fix Windows drive letter issue (e.g., "C:xampp" issue)
        if (strpos($cwd, ':') === 1) { // If there's a missing backslash after drive letter
            $cwd = strtoupper($cwd[0]) . ":\\" . substr($cwd, 2);
        }

        return $cwd;
    } else {
        return "Error: Directory not found or permission denied!";
    }
}

echo cd('__path__');