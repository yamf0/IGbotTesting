from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from time import sleep
import os


class driveFile():
    """
        This class will upload and download files from Drive
    """    
    def __init__(self, obj):
        """
            Authenticate Login for first time, then ist automatically
        """
        self.obj = obj
        self.username = obj.username
        self.thisRunFolder = None
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
        file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        
        for file in file_list:
            if (file['title'] == self.username and file['mimeType'] == "application/vnd.google-apps.folder"):        
                print("Folder already exists")
                self.thisRunFolder = file
            
        #Create a Folder with the name of the account 
        if self.thisRunFolder is None:
            self.thisRunFolder = self.drive.CreateFile({'title' : self.username, 'mimeType' : "application/vnd.google-apps.folder" })
            self.thisRunFolder.Upload()
           
        

    def downloadFile(self, fileNames):
        """
            Download specified Filename from drive

            variables 
            ->fileName:  name of file to be downloaded

            Return:
            ->1 :  File was downloaded
            ->0 : File couldnt be found
        """
        for file in fileNames:
            try:
                os.remove(file)
            except:
                print("File does not existed previously")
        
        #Get Files within this run folder
        file_list = self.drive.ListFile({'q': "'{}' in parents and trashed=false".format(self.thisRunFolder["id"])}).GetList()


        existsFile = 0
        for finFolder in file_list:

            for file in fileNames:
                print(file)
                if (finFolder['title'] == file):
                    finFolder.GetContentFile(str(file))
                    existsFile = 1

        for file in fileNames:
            if (os.path.exists(file)):
                ##Code Error 1 means success##
                return 1
            elif(existsFile == 0):
                return 1
            else: 
                print ("File was not downloaded, please re run code")
                sleep(10)
                return 0

    def uploadFile (self, fileNames):
        """
            Deletes from drive file and the Upload from local

            Variables
            ->fileName: file to upload

            Return:
            ->1 :  File was downloaded
            ->0 : File couldnt be found
        """
        file_list = self.drive.ListFile({'q': "'{}' in parents and trashed=false".format(self.thisRunFolder["id"])}).GetList()

        for finFolder in file_list:
            for file in fileNames:
                if (finFolder["title"] == file):
                    finFolder.Delete()

        
        for file in fileNames:
            print("Uploading to Drive {}".format(file))
            newFile = self.drive.CreateFile({"title" : file, "parents": [{"id": self.thisRunFolder["id"]}] })
            newFile.SetContentFile(file)
            try:
                newFile.Upload()  
            ##Catch exception of not upload possible##
            except:
                print("File was unable to upload")
                #return 0
        return 1




