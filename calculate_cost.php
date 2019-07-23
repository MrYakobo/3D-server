<?php

define("UPLOAD_DIR", "files/");
// define("STL_HEADER", "libthing_export");

function calculate_cost($target){
    passthru("./stats.sh '$target'");
}

function upload($tmp, $target){
    $status = move_uploaded_file($tmp, $target);
    return $status;
}

function validate($tmp, $target){
    if (count($_FILES) == 0) return "No file uploaded";

    $ext = strtolower(pathinfo($target, PATHINFO_EXTENSION));

    if ($ext != "stl") return "Must have .stl-extension"; // måste vara .stl-extension

    /*
    $fp = fopen($tmp, 'r');
    $header = fread($fp, 15);   // läs 15 bytes (header)
    fclose($fp);

    if ($header != STL_HEADER) return "Must have stl header";

    if(file_exists($target)) return "File already exists";
    */

    return "";
}

$tmp = $_FILES["file"]["tmp_name"];
$target = UPLOAD_DIR . basename($_FILES["file"]["name"]);

$err = validate($tmp, $target);

if ($err != "")
    die("ERR: " . $err);

$err = upload($tmp, $target);

if (!$err)
    echo "ERR: Upload failed";

?>
<pre>
<?php calculate_cost($target); ?>
</pre>
