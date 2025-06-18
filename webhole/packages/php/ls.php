<?php
$path = '__path__';

if (!is_dir($path)) {
    echo json_encode(["[✗] The Directory '{$path}' does not exist"]);
    exit();
}

$fileList = array();

if ($handle = opendir($path)) {
    while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
            if (is_dir($path . DIRECTORY_SEPARATOR . $entry)) {
                $fileList[] = "📁 " . $entry; // Folder emoji
            } else {
                $fileList[] = "📄 " . $entry; // File emoji
            }
        }
    }
    closedir($handle);
}

echo json_encode($fileList);

