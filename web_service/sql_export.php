<?php

$lengthlimit = 2048;
if (isset($_GET["modelYamlUrl"]))
{
  $modelYamlUrl =  $_GET["modelYamlUrl"];
}
if (isset($_GET["email"]))
{
  $email = $_GET["email"];
}

if ((strlen($modelYamlUrl) < $lengthlimit) && (strlen($email) < $lengthlimit))
{
  if (filter_var($modelYamlUrl, FILTER_VALIDATE_URL))
  {
    //  header('Content-Type: application/json; charset=utf-8');
    header('Content-Type: text/event-stream');
    header('Cache-Control: no-cache');

    //$command = "sudo /usr/bin/python3 /home/fiware/production/tests/master_tests.py ".$modelYamlUrl." ".$email." ".$testnumber." >> /var/www/html/extra/mastercheck_output/master_check-`date +\%Y-\%m-\%d_\%H-\%
M-\%S`.txt 2>&1 &";
    $command = "sudo /usr/bin/python3 /home/fiware/production/sql_export.py ".$modelYamlUrl ;
    // $command = escapeshellcmd($baseCommand);
    $outputs = exec($command);
    echo '<pre style="white-space: pre-wrap; word-wrap: break-word;">';
    echo($outputs);
    echo '</pre>';
    }
  }

else {
  // header('Content-Type: application/json; charset=utf-8');
  header('Content-Type: text/event-stream');
  header('Cache-Control: no-cache');
  print("{\"url too large\"}");
}

?>
