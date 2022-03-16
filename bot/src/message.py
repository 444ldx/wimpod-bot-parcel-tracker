import discord
from datetime import datetime

class Message:
    def __init__(self, args:dict={"":""}):
        self.args = args

    def welcome(self):
        """Send an embed for welcome

        Returns:
            Embed: Welcome
        """
        message = discord.Embed()
        message.color = int("F4D03F", base=16)
        message.set_author(name="Wimpod", icon_url="https://ldxdev.github.io/wimpod/img/wimpod_logo.png")
        message.add_field(name="Salut, moi c'est Wimpod", value="""
                          Je suis ton assistant de suivis de colis intégré à Discord ^^
                          Tu peux exécuter la commande /suivis pour suivre ton colis ou la commande /aide pour avoir la liste des commandes !
                          """)
        message.set_footer(text="Version BETA 1.0")
        return message
        
    def credit(self):
        """Send an embed with the credits

        Returns:
            Embed: Informations
        """
        message = discord.Embed()
        message.color = int("F4D03F", base=16)
        message.set_author(name="Wimpod", icon_url="https://ldxdev.github.io/wimpod/img/wimpod_logo.png")
        message.add_field(name="Description", value="""
                          Je suis un bot de suivis de colis sur Discord intégrant l'API de la Poste.
                          J'ai été programmé en Python 3.7.9 par LDX#4009, un étudiant de première ^^
                          Si vous avez des suggestions ou des questions vous pouvez effectuer la commande de suggestion intégré à moi,et si tu souhaitez nous soutenir tu peux effectuer la commande de dons <3
                          """)
        message.set_footer(text="Version BETA 1.0")
        return message

    def aide(self):
        """Send an embed with help

        Returns:
            Embed: Help
        """
        message = discord.Embed()
        message.color = int("F4D03F", base=16)
        message.set_author(name="Wimpod", icon_url="https://ldxdev.github.io/wimpod/img/wimpod_logo.png")
        message.add_field(name="/suivis [NUMERO]", value="""
                          Cette commande te permet de suivre ton colis du service de la Poste.
                          Remplacer [NUMERO] par le numéro de suivis de 11 à 15 caractères alphanumériques.
                          """, inline=False)
        message.add_field(name="/suggestion [MESSAGE]", value="""
                          Cette commande te permet d'envoyer une question ou une suggestion.
                          Remplacer [MESSAGE] par votre message
                          """,inline=False)
        message.add_field(name="/don", value="""
                          Cette commande te permet d'obtenir le lien de don.
                          """,inline=False)
        message.set_footer(text="Version BETA 1.0")
        return message

class MessageLaPoste:
    def __init__(self, response:dict):
        self.response = response

    def success(self):
        """Send an embed when requesting successful follow-ups

        Returns:
            Embed: Parcel Informations
        """
        if self.response.get("entryDate") != "pas encore":
            date = "le " + datetime.strptime(self.response.get("entryDate")[0:-3] + "00", "%Y-%m-%dT%H:%M:%S%z").strftime("%m/%d/%Y %H:%M:%S")
        else:
            date = self.response.get("entryDate")
        
        message = discord.Embed()
        message.color = int("F4D03F", base=16)
        message.set_author(name=self.response.get('product').capitalize(), icon_url="https://ldxdev.github.io/wimpod/img/poste_logo.jpg")
        message.add_field(name="Informations :", value="Réceptionné par la Poste : " + date)
        i = 1
        for event in reversed(self.response.get("event")):
            date1 = datetime.strptime(event.get("date")[0:-3] + "00", "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%Y %H:%M:%S")
            message.add_field(name= "Etape " + str(i) + " | " + event.get('code').replace('DR1', 'Déclaratif réceptionné')
                .replace('PC1', 'Pris en charge')
                .replace('PC2', 'Pris en charge dans le pays d’expédition')
                .replace('ET1', 'En cours de traitement')
                .replace('ET2', 'En cours de traitement dans le pays d’expédition')
                .replace('ET3', 'En cours de traitement dans le pays de destination',)
                .replace('ET4', 'En cours de traitement dans un pays de transit',)
                .replace('EP1', 'En attente de présentation',)
                .replace('DO1', 'Entrée en Douane',)
                .replace('DO2', 'Sortie  de Douane')
                .replace('DO3', 'Retenu en Douane')
                .replace('PB1', 'Problème en cours')
                .replace('PB2', 'Problème résolu')
                .replace('MD2', 'Mis en distribution')                     
                .replace('ND1', 'Non distribuable')
                .replace('AG1', 'En attente d\'être retiré au guichet')
                .replace('RE1', 'Retourné à l\'expéditeur')
                .replace('DI1', 'Distribué')
                .replace('DI2', 'Distribué à l\'expéditeur') + " | le " + date1,
                value=event.get("label"), inline=False)
            i = i+1
        message.set_footer(text=f"{self.response.get('product').capitalize()} : {self.response.get('idShip')}")
        return message

    def error(self):
        """Send an integration during a failed follow-up request

        Returns:
            Embed: Error Informations
        """
        message = discord.Embed()
        message.color = int("F4D03F", base=16)
        message.set_author(name="La Poste", icon_url="https://ldxdev.github.io/wimpod/img/poste_logo.jpg")
        message.add_field(name="Oups, erreur lors de la demmande suivis !", value=self.response.get("message"))
        message.set_footer(text=f"Suivis : {self.response.get('idShip')}")
        return message

    def id_not_define(self):
        """Send an integration when no id has been entered

        Returns:
            Embed: Error Informations
        """
        message = discord.Embed()
        message.color = int("F4D03F", base=16)
        message.set_author(name="Wimpod", icon_url="https://ldxdev.github.io/wimpod/img/poste_logo.jpg")
        message.add_field(name="Tu dois spécifier un numéro de suivis !", value="Compris entre 11 et 15 caractères alphanumériques (Exemple : EP111111110FR)")
        message.set_footer(text="Erreur")
        return message