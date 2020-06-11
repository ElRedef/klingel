Write-Host "Running Flask"
$env:FLASK_APP = "klingel"
$env:FLASK_ENV = "development"
$env:MY_PATH = "Beispielpfad"

flask run