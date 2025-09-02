Write-Host "Running Flask"
$env:FLASK_APP = "klingel"
$env:FLASK_ENV = "development"
$env:KLINGEL_SETTING_FILE = "C:\Users\xxx\Programming\hausautomatisierung\klingel\configwin.json"


#set FLASK_APP=klingel
#set FLASK_ENV=development

flask run