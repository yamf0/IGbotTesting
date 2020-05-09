from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from time import sleep



class driveFile():
    """
        This class will upload and download files from Drive
    """    
    def __init__(self):
        """
            Authenticate Login for first time, then ist automatically
        """
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

        self.drive = GoogleDrive(gauth)
        ##returns a list of all files in Drive##
        self.file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    def downloadFile(self, fileName):
        """
            Download specified Filename from drive

            variables 
            ->fileName:  name of file to be downloaded
        """
        
        for file1 in self.file_list:
            if (file1['title'] == fileName):
                file1.GetContentFile(str(fileName))

    def uploadFile (self, fileName):
        """
            Deletes from drive file and the Upload from local

            Variables
            ->fileName: file to upload
        """
        for file1 in self.file_list:
            if (file1["title"] == fileName):
                file1.Delete()

        print("Uploading Drive")
        file = self.drive.CreateFile()
        file.SetContentFile(fileName)
        file.Upload()  
        sleep(2)




