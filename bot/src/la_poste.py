import os
from message import MessageLaPoste
from dotenv import load_dotenv
from discord.ext import commands
import requests

load_dotenv(dotenv_path="config")

class Poste:
    def __init__(self, parcel_id:str, lang:str="fr_FR"):
        self.parcel_id = parcel_id
        self.lang = lang
    
    def url(self):
        """Formatting the request URL

        Returns:
            str: URL
        """
        return os.getenv("URL") + "suivi/v2/idships/"+ self.parcel_id + "?lang=" + self.lang

    def params(self):
        """Formatting request arguments

        Returns:
            str: Arguments
        """
        return {"Accept": os.getenv("APPLICATION"), "X-Okapi-Key": os.getenv("OKAPI")}

    def tracker(self):
        """Track a parcel

        Returns:
            dict: Parcel informations
        """
        response = requests.get(self.url(), headers=self.params())

        response.encoding = "utf-8"
        json_response = response.json()

        if response.status_code == 200 or response.status_code == 207:

            shipment = json_response.get("shipment")

            return MessageLaPoste({"idShip": shipment.get("idShip", "Numéro introuvable"),
                "product": shipment.get("product", "Produit introuvable"),
                "entryDate": shipment.get("entryDate", "pas encore"),
                "event": shipment.get("event")}).success()
        else:
            idShip = json_response.get("idShip", "Numéro introuvable")
            message = json_response.get("returnMessage", "Erreur")
            return MessageLaPoste({"idShip": idShip,
                "message": message}).error()


if __name__ == "__main__":
    test = Poste("9V31967384377")
    print(test.tracker())