import argparse
from time import sleep
from igStart import igStart
from igProfile import igProfile
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
    parser.add_argument("-d", "--drive", help="Will drive download Info", default=False, action="store_true")
    parser.add_argument("-l", "--likedphotos", help="will enter most liked fotos at iteration", default=False, action="store_true")

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
        Bot = igStart(account, password, args)
    
    Perfil = igProfile(Bot)
    Perfil.iterarPerfil(Bot)
    sleep(5)
    
    #TODO crear instancia de iginteraction y ver lo de los objetos internos y json objetos
    """
    Iterar = igInteraction(Bot)

    for i in range (4):
        logger.info("Hashtag number: {} ".format(i))
        Iterar.iterateHastag(Bot.jsonObj.generateHashtag())
        Bot.jsonObj.writeInfo(Bot.fileNameRoot, "w", Bot.permaData)

    if Bot.runDrive == True:
        Bot.driveObj.uploadFile(Bot.fileNames) """

    #Cierre de instancia del web driver 
    Bot.driver.quit()


if __name__ == "__main__":
    main()