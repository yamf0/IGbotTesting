import argparse
from time import sleep
from igStart import igStart
from igProfile import Profile
from igInteraction import igInteraction
from igJSON import jsonConstructor
import logging
import logging.config

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('root')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--account", help="Account to run (m for MexicanTest, d for GermanyTest, Account name for other)")
    parser.add_argument("-p", "--password", help="Password to account", default= None)
    #parser.add_argument("-d", "--drive", help="Will drive download Info", default=False, action="store_true")

    args = parser.parse_args()

    if (args.account == "m"):
        Bot = igStart('photoandtravel2020','mannheimzittau', args)
    
    elif (args.account == "d"):
        Bot = igStart('travelandphoto2020','mannheimzittau', args)
    else:
        account = args.account
        password = args.password
        print("You entered: " + account)
        print("You entered: " + password)
        sleep(2)
        Bot = igStart(account,password, args)
    
    Perfil = Profile(Bot)
    Perfil.iterarFotos(Bot)
    sleep(5)
    #TODO Cambiar esto apra que se mande a llamar desde el main Aqui iteramos en el init (esta mal)
    for i in range (4):
        logger.info("Hashtag number: {} ".format(i))
        igInteraction.iterateHastag(jsonConstructor.generateHashtag())
        jsonConstructor.writeInfo(igStart.fileNameRoot, "w", igStart.permaData)

    #TODO migrar a main
    if self.runDrive == True:
        self.driveObj.uploadFile(self.fileNames)

    #Ciere de instancia del web driver 
    Bot.driver.quit()


if __name__ == "__main__":
    main()