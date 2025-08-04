<html>
<head>
	<title>You shall not pass!</title>
  <meta charset="UTF-8">
</head>
<body>
  <h1>Login:</h1>
	<input type="password" id="password" placeholder="Password" />
	<button onclick="passwordcheck()">Submit</button>
</body>
<script>
function passwordcheck() {
	var password = document.getElementById("password").value;
	if (password === "letmein1234!") {
		window.location.href = "/flag.php";
	} else {
		alert("Incorrect password. You shall not pass!");
	}
}
</script>
</html>
