<?php
    include 'db.php';
    include 'data.php';

    session_start();

    $db = new DB();
    $file = "cert.bak";
    $userid = $_SESSION["user"]->id;
    $data = $db->get_certificates($userid);
    // echo $data;
    $sData = serialize($data);
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="backup_certificates"');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    // header('Content-Length: ' . sizeof($sData));
    echo $sData;
?>