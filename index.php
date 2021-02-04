<?php
require 'dbConf.php';

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT lumimaara FROM lumi";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo "<p class='currentLumi'>Lunta nyt: " . $row["lumimaara"] . " mm</p>";
  }
} else {
  echo "0 results";
}
?>
<html>
  <head>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
  <br><br><br><br>
  <center>
  <form action="">
    <label for="search">Search (yyyy-mm-dd):</label>
    <input type="text" id="search" name="search"><br><br>
    <input type="submit" value="Submit">
  </form>
  <br>  <br>  <br>
  <?php
  echo $_GET['search'];
  ?>
  <br>  <br>  <br>
  <div class="paivaTaulukko">
    <table style="width:1200px">
      <tr>
        <th>0</th>
        <th>1</th>
        <th>2</th>
        <th>3</th>
        <th>4</th>
        <th>5</th>
        <th>6</th>
        <th>7</th>
        <th>8</th>
        <th>9</th>
        <th>10</th>
        <th>11</th>
        <th>12</th>
        <th>13</th>
        <th>14</th>
        <th>15</th>
        <th>16</th>
        <th>17</th>
        <th>18</th>
        <th>19</th>
        <th>20</th>
        <th>21</th>
        <th>22</th>
        <th>23</th>
      </tr>
      <tr>
        <?php
          $sql = "SELECT lumimaara FROM historia WHERE date >= '" . $_GET['search'] . " 0:00:00' and date <= '" . $_GET['search'] . " 23:59:00'";
          $result = $conn->query($sql);
          
          if ($result->num_rows > 0) {
            // output data of each row
            $idNum = 0;
            while($row = $result->fetch_assoc()) {
                echo "<td id='hour" . $idNum . "'>" . $row["lumimaara"] . " mm</td>";
                $idNum += 1;
            }
          } else {
            echo "0 results";
          }
        ?>
      </tr>
    </table> 
  </div>
  <p id="paivanKeskiarvo">11 mm</p>
  <canvas id="sCanvas" width="1200" height="500" style="border:1px solid #d3d3d3;">
  <script type="text/javascript" src="scripts.js"></script>
  </center>
  </body>
</html>

<?php
$conn->close();
?>