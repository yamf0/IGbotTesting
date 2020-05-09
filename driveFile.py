from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from time import sleep
gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

requestedFile = "photoinfo.json"
updateFile = "photoinfo.json"
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    if (file1['title'] == requestedFile):
        file1.GetContentFile(str(requestedFile))
    print('title: %s, id: %s' % (file1['title'], file1['id']))

    if (file1["title"] == updateFile):
        file1.Delete()

sleep(10)
file = drive.CreateFile()
file.SetContentFile("photoinfo.json")
file.Upload()    

#### Delete File




