import discord
import os
from keep_alive import keep_alive
import random
import requests
# Allows to make HTTP requests which gives JSON back
import json
# JSON is a module for storing and transferring data
from replit import db

# Connection to discord
client = discord.Client()

sad_words = ["lonely" "heartbroken", "gloomy", "disappointed", "hopeless", "grieved", "unhappy", "lost", "troubled", "resigned", "miserable", "sad", "depressed", "bad", "sucky"]

starter_encouragements = [
    'Cheer up friend!',
    'You got this!',
    'You are halfway there!',
    'Hang in there bud!',
    "You ain't alone!",
    "We're all in the same boat!",
    "It will get better eventually!",
    "If its not better, then its not the end. Good things come to those who wait!",
    "Forget about your worries for a while and sleep!",
    'Get some air, surely it will make you feel better!'
]

my_secret = os.environ['TOKEN']

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():

    # this line fetches random quote from url given
    response = requests.get("https://zenquotes.io/api/random")

    # Convert the response into json
    json_data = json.loads(response.text)

    # 'q' is the key for the value containing the quote which it obtained from json_data. " -" is for showing who wrote the quote. 'a' is for author of the quote
    quote = json_data[0]['q'] + '  ~' + json_data[0]['a']
    return quote

# encouraging_message is given by user 
def update_encouragements(encouraging_message):

    # db.keys() returns a list of keys from a database
    # checks if encouragements is in db.keys()
    if 'encouragements' in db.keys():

        # set the database to variable 'encouragements' to access its key value pairs
        encouragements = db['encouragements']

        # adding the new encouragement
        encouragements.append(encouraging_message)

        # saving the database after appending new encouragement aka updation
        db['encouragements'] = encouragements

    # if there are no encouragements, then we create it using a list which contains the encouraging_message
    else:
        db['encouragements'] = [encouraging_message]
    
def delete_encouragements(index):

    # instantiating the db with variable for access to its key value pairs
    encouragements = db['encouragements']

    # length of encouragements shouldn't be more than the index because a user can pass an index which isn't there in the list, for that we can delete the message at that index
    if len(encouragements) > index:
        del encouragements[index]

        # updating the database
        db['encouragements'] = encouragements

# registering an event
@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event

async def on_message(message):

    msg = message.content
    
    if db["responding"] == True:
        options = starter_encouragements
        if 'encouragements' in db.keys():
            options += db['encouragements']

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if message.author == client.user:
        return
    
    if msg.startswith('$hello'):
        await message.channel.send("Hey! How you doin'?")

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if msg.startswith('$new'):
        # Here we split '$new ' with space because we only want tto store the message in the database excluding the extra space in the begginning
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send('New encouraging message added =D')
    
    if msg.startswith('$del'):
        encouragements = []
        # If there is no encouragement in the database already, it will return an empty list and if the encouragement is there it will simply return that one
        if "encouragements" in db.keys():
            index = int(msg.split("$del", 1)[1])
            delete_encouragements(index)
            encouragements = db['encouragements']
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]
        
        if value.lower() == 'true':
            db["responding"] = True
            await message.channel.send("Responding is ON")
        else:
            db["responding"] = False
            await message.channel.send("Responding is OFF")

    if msg.startswith("$help"):
        await message.channel.send("""
```        Commands :-
        
$hello -> greeting
$inspire -> to get inspirational quote
$new -> to add a new encouraging message
$del -> to delete an encouragingmessage 
$list -> to list all encouragements
$responding -> to check if bot is responding or not

If the bot detects a sad word, it will send an encouragement.

Try < I feel sad >```
        """)

keep_alive()
client.run(os.environ['TOKEN'])
