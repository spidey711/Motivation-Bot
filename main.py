import discord
import os
from keep_alive import keep_alive
import random
import requests
import json
from replit import db

my_secret = os.environ['TOKEN']
client = discord.Client()

sad_words = [
    'sadden', 'sad', 'unhappy', 'suck', 'lonely', 'alone', 'mournful',
    'melancholy', ' down ', 'doleful', 'downcast', 'gloom', 'glum', 'gloomy',
    'sorrowful', 'sorrow', 'dejected', 'rejected', 'desolate', 'downhearted',
    'broken heart', 'depressed', 'tragic', 'disconsolate', 'dreary',
    'lonesome', 'tragedy', 'sorry', 'lugubrious', 'sadness', 'wistful',
    'sadly', 'lachrymose', 'heavy hearted', 'heavy-hearted', 'depress',
    'plaintive', 'howl', 'dusky', 'dismal', 'demise', 'somber', 'moody',
    'tearjerker', 'inconsolable', 'crestfallen', 'regret', 'joyless',
    'messed up', 'plangent', 'down in the mouth', 'woebegone', 'woeful',
    'tearful', 'elegy', 'heartbroken', 'yowl', 'low-spirited', 'low spirited',
    'long face', 'sad-assed', 'sombre', 'suicide', 'suicidal', 'upset',
    'sucky', 'dammit', 'bad'
]

starter_encouragements = [
    "It will be alright.", "Keep going!", "You got this!", "Never give up!",
    "You're on your way.", "Go sleep for a while.",
    "If its not better, then its not the end.",
    "First step is always the hardest.", "Go take a walk.",
    "You're not alone.", "Don't, under any circumstances, give up!",
    "I'm with you.", "It's ok, shit happens sometimes.",
    "Go play games or something, it will take you mind off of things",
    "Screw everything and go do something you love, you will probably feel better",
    "Listen to music and chill out."
]

user_greetings = ['$hello',"$hi","$hey","$hola","$salut","$kon'nichiwa"]

greetings = [
    'Hey!', "👋🏻", 'How are you today?', 'Hi there!', "Hola!",
    "Kon'nichiwa(⌐■_■)", "How's it going?"
]

if "responding" not in db.keys():
    db["responding"] = True


def embed_help():
    embed = discord.Embed(
        title="𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎",
        color=discord.Color.from_rgb(255, 126, 0))
    embed.add_field(name="𝙎𝙩𝙖𝙣𝙙𝙖𝙧𝙙", value="$hello to greet bot\n$use to get this embed", inline=False)
    embed.add_field(name="𝙄𝙣𝙨𝙥𝙞𝙧𝙖𝙩𝙞𝙤𝙣", value="$inspire to get an inspirational quote", inline=False)
    embed.add_field(name="𝙐𝙩𝙞𝙡𝙞𝙩𝙮", value="$new to add encouraging message\n$list to see a list of added messages\n$del [index of added message] to delete message\n$responding true to turn ON Auto-Responding Feature\n$responding false to turn OFF Auto-Responding Feature", inline=False)
    embed.set_footer(text="AUTO RESPONDING FEATURE:-\nThis feature allows the bot to respond automatically if it detects a sad word in a user's sentence. Try 'I am sad'")
    embed.set_thumbnail(url="https://unsplash.com/photos/XMcoTHgNcQA")
    return embed


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + '  ~' + json_data[0]['a']
    return quote


def update_encouragements(encouraging_message):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(encouraging_message)
        db['encouragements'] = encouragements
    else:
        db['encouragements'] = [encouraging_message]


def delete_encouragements(index):
    encouragements = db['encouragements']
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements


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
        if any(word in msg.lower() for word in sad_words):
            await message.channel.send(random.choice(options))
    
    if message.author == client.user:
        return
    
    if 1:
        for greet in user_greetings:
    
            if msg.startswith(greet):
                await message.channel.send(random.choice(greetings))
    
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(embed=discord.Embed(description=quote, color=discord.Color.from_rgb(255, 126, 0)))
    
    if msg.startswith('$new'):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send('New encouraging message added.')
    
    if msg.startswith('$del'):
        encouragements = []
    
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
            await message.channel.send(embed=discord.Embed(description="Responding is ON", color=discord.Color.from_rgb(255, 126, 0)))
        else:
            db["responding"] = False
            await message.channel.send(embed=discord.Embed(description="Responding is OFF", color=discord.Color.from_rgb(255, 126, 0)))
    
    if msg.startswith('$use'):
        await message.channel.send(embed=embed_help())


keep_alive()
client.run(os.environ['TOKEN'])
