<?php

function get_dir_tree(string $dir_path = './', bool $relative_path = true): string {
    $base_path = realpath($dir_path);
    if ($base_path === false || !is_dir($base_path)) {
        return "❌ The directory '{$dir_path}' does not exist.";
    }

    if (!is_readable($base_path)) {
        return "❌ The directory '{$dir_path}' is not accessible.";
    }

    $lines = [];

    $render_tree = function (string $current_path, string $prefix = '') use (&$render_tree, $base_path, $relative_path, &$lines) {
        $entries = scandir($current_path);
        if ($entries === false) {
            $lines[] = $prefix . "❌ Error reading directory: {$current_path}";
            return;
        }

        $entries = array_filter($entries, fn($e) => $e !== '.' && $e !== '..');

        $dirs = [];
        $files = [];

        foreach ($entries as $entry) {
            $full = $current_path . DIRECTORY_SEPARATOR . $entry;
            if (is_dir($full)) {
                $dirs[] = $entry;
            } else {
                $files[] = $entry;
            }
        }

        sort($dirs);
        sort($files);
        $all = array_merge($dirs, $files);
        $total = count($all);

        foreach ($all as $index => $entry) {
            $is_last = $index === $total - 1;
            $connector = $is_last ? '└── ' : '├── ';
            $child_prefix = $prefix . ($is_last ? '    ' : '│   ');
            $full_path = $current_path . DIRECTORY_SEPARATOR . $entry;

            $display_path = $relative_path ? $entry : $full_path;
            $lines[] = $prefix . $connector . $display_path;

            if (is_dir($full_path)) {
                $render_tree($full_path, $child_prefix);
            }
        }
    };

    $lines[] = $relative_path ? basename($base_path) : $base_path;
    $render_tree($base_path);

    return implode(PHP_EOL, $lines);
}

// Example usage
echo get_dir_tree('__path__', true); // Replace 'Tasks' with your target directory

?>
