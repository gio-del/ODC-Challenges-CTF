<?php
class DB{
    private $mysqli;

    function __construct(){
        $dbhost = $_ENV["DBHOST"];
        $dbuser = $_ENV["DBUSER"];
        $dbpass = $_ENV["DBPASS"];
        $db = $_ENV["DBNAME"];
        $this->mysqli = new mysqli($dbhost, $dbuser, $dbpass,$db) or die("Connect failed: %s\n".  $this->mysqli -> error);
    }

    
    function __destruct()
    {
        $this->mysqli -> close();
    }
    

    function create_user($name, $password){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("INSERT INTO users(name, password) VALUES (?, ?)"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
            die();
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("ss", $name, $password)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            die();
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
            die();
        }

    }



    function login($name, $password){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT idusers FROM users WHERE name=? and password=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("ss", $name, $password)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $info = $res->fetch_assoc();

        $userid = $info['idusers'];
        $res->close();
        return $userid;
    }

    function get_username($id){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT name FROM users WHERE idusers=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("i", $id)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $info = $res->fetch_assoc();

        $name = $info['name'];
        $res->close();
        return $name;
    }

    function get_idusers($name){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT idusers FROM users WHERE name=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("s", $name)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $info = $res->fetch_assoc();

        $id = $info['idusers'];
        $res->close();
        return $id;
    }

    function create_certificate($userid, $name, $expire_date){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("INSERT INTO certificates(name, expire_date, user_id) VALUES (?, ?, ?)"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("ssi", $name, $expire_date, $userid)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

    }

    function get_certificates($userid){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT idcertificates, name, expire_date FROM certificates WHERE user_id=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("i", $userid)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $info = $res->fetch_all(MYSQLI_ASSOC);

        $res->close();
        return $info;
    }


}
?>