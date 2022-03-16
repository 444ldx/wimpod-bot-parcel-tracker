import os
import logging
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from la_poste import Poste
from message import MessageLaPoste
from message import Message
from data import Data

load_dotenv(dotenv_path="config")
logging.basicConfig(filename='bot.log', format='[%(levelname)s %(asctime)s] %(message)s', level=logging.INFO)

client = commands.Bot(command_prefix=os.getenv("PREFIX"))

@client.event
async def on_ready():
    logging.info(f"{client.user.name} is online !")
    client.loop.create_task(status_task())

async def status_task():
    """Status update
    """
    while True:
        await client.change_presence(activity=discord.Game("Envoie moi un DM"))
        await asyncio.sleep(5.0)
        await client.change_presence(activity=discord.Game("Suivis de colis"))
        await asyncio.sleep(10.0)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Messages received in DM
    if isinstance(message.channel, discord.channel.DMChannel):
        Data("use_bot.txt").log()
        
        if message.content.startswith("/suivi"):
            Data("use_suivis.txt").log()
            parcel_id = message.content[8:]
            if parcel_id == "":
                await message.channel.send(embed=MessageLaPoste({"id": parcel_id}).id_not_define())
            else:
                await message.channel.send(embed=Poste(parcel_id=parcel_id.replace(" ", "_")).tracker()) 
                logging.info(f"{message.author.name} has requested follow-ups with number '{parcel_id}'")  
                
        elif message.content.startswith("/credit"):
            logging.info(f"{message.author.name} use command /credit")  
            await message.channel.send(embed=Message().credit())    
                
        elif message.content.startswith("/aide") or message.content.startswith("/help"):
            logging.info(f"{message.author.name} use command /aide")
            await message.channel.send(embed=Message().aide())      
                  
        elif message.content.startswith("/suggestion"):
            logging.info(f"{message.author.name} use command /credit")      
            if message.content[12:] != "":
                Data(fichier="suggestion.txt", user=message.author.name + "#" + message.author.discriminator, text=message.content[13:]).suggestion()
                await message.channel.send("Ton commentaire à été envoyé ! Merci <3")
            else:
                await message.channel.send("Tu dois spécifier un message")
                
                
        elif message.content.startswith("/don"):
            logging.info(f"{message.author.name} use command /aide")
            await message.channel.send("Merci beaucoup pour le soutiens <3 \nhttps://paypal.me/johanledoux?country.x=FR&locale.x=fr_FR") 
               
        else:
            await message.channel.send(embed=Message().welcome())
            logging.info(f"Welcome {message.author.name}")

            
    # Messages received on a server
    else:
        Data("use_bot.txt").log()
        if message.content.startswith("/suivi"):
            Data("use_suivis.txt").log()
            parcel_id = message.content[8:]
            if parcel_id == "":
                await message.author.send(embed=MessageLaPoste({"id": parcel_id}).id_not_define())
            else:
                await message.author.send(embed=Poste(parcel_id=parcel_id).tracker())   
                logging.info(f"{message.author.name} has requested follow-ups with number '{parcel_id}'") 
                
        elif message.content.startswith("/credit"):
            logging.info(f"{message.author.name} use command /credit") 
            await message.author.send(embed=Message().credit())        
               
        elif message.content.startswith("/aide") or message.content.startswith("/help"):
            logging.info(f"{message.author.name} use command /aide") 
            await message.author.send(embed=Message().aide())     
                   
        elif message.content.startswith("/suggestion"):
            if message.content[12:] != "":
                Data(fichier="suggestion.txt", user=message.author.name + "#" + message.author.discriminator, text=message.content[13:]).suggestion()
                await message.author.send("Ton commentaire à été envoyé ! Merci <3")
                logging.info("A suggestion has been sent")
            else:
                await message.author.send("Tu dois spécifier un message")
                
        elif message.content.startswith("/don"):
            logging.info(f"{message.author.name} use command /don") 
            await message.author.send("Merci beaucoup pour le soutiens <3 \nhttps://paypal.me/johanledoux?country.x=FR&locale.x=fr_FR")
        
client.run(os.getenv("TOKEN"))

