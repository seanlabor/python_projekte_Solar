<?php

$Tracelevel = 8;

$funktionen = new funktionen ();

$funktionen-> log_schreiben("Befehl an Boiler zum aufheizen geschickt",5);

// URL to which you want to send the POST request
$url = 'https://enyl64kyq1fhe.x.pipedream.net';

// Data to be sent in the POST request (if any)
$postData = [
    'key1' => 'value1',
    'key2' => 'value2',
];

// cURL initialization
$ch = curl_init($url);

// Set cURL options
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

// Execute cURL session and get the response
$response = curl_exec($ch);

// Check for cURL errors
if (curl_errno($ch)) {
    echo 'cURL Error: ' . curl_error($ch);
}

// Close cURL session
curl_close($ch);

?>