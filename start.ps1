Write-Host "Running Flask"
$env:FLASK_APP = "klingel"
$env:FLASK_ENV = "development"
$env:KLINGEL_SETTING_FILE = "C:\Users\Johannes\Programming\hausautomatisierung\klingel\config.json"

flask run