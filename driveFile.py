from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from time import sleep
import os


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

            Return:
            ->1 :  File was downloaded
            ->0 : File couldnt be found
        """
        try:
            os.remove(fileName)
        except:
            print("File does not existed previously")
        existsFile = 0
        for file1 in self.file_list:
            if (file1['title'] == fileName):
                file1.GetContentFile(str(fileName))
                existsFile = 1

        if (os.path.exists(fileName)):
            ##Code Error 1 means success##
            return 1
        elif(existsFile == 0):
            return 1
        else: 
            print ("File was not downloaded, please re run code")
            sleep(10)
            return 0

    def uploadFile (self, fileName):
        """
            Deletes from drive file and the Upload from local

            Variables
            ->fileName: file to upload

            Return:
            ->1 :  File was downloaded
            ->0 : File couldnt be found
        """
        for file1 in self.file_list:
            if (file1["title"] == fileName):
                file1.Delete()

        print("Uploading Drive")
        file = self.drive.CreateFile()
        file.SetContentFile(fileName)
        try:
            file.Upload()  
        ##Catch exception of not upload possible##
        except drive.ApiRequestError as ex:
            print("File was unable to upload with : {}".format(ex))
            return 0
        return 1




