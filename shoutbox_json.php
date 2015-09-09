<?php
require "backend/functions.php";
dbconn();

$query = "select msgid,user,message,date from shoutbox order by date desc limit 20";
$result = SQL_Query_exec($query);
$return_arr = array();
while ($row = mysql_fetch_assoc($result)) {
  $row_array['id'] = $row['msgid'];
  $row_array['user'] = $row['user'];
  $row_array['message'] = $row['message'];
  array_push($return_arr,$row_array);
}
echo json_encode($return_arr);
?>
