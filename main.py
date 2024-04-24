import discord
import os
from discord.ext import commands
import google.generativeai as genai

genai.configure(api_key="AIzaSyDU8CmoR5leSj46dumaU1U5lYSmCUdg0-w")

safety_settings = [
    {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
    {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
    {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        }
    ]

model = genai.GenerativeModel('gemini-pro', safety_settings)

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your Discord bot token
TOKEN = 'ODg3NjI4OTAwMTExMzYwMDcw.GBbzm-.iCYu-EESOJg4G3khkVuFyQIEEqSeciEDIE-A0A'

# ID to clear messages after
CLEAR_ID = 848616447902613544

# Initialize Discord client
client = commands.Bot(command_prefix='$', intents=discord.Intents.all())

def get_intro_message():
    with open("rules.txt", "r") as file:
        return file.read()

def log_message(message):
    with open("messagelog.txt", "a") as file:
        file.write(f"{message.content}\n")

def clear_messages():
    with open("messagelog.txt", "w") as file:
        file.write("")

def get_logged_messages():
    with open("messagelog.txt", "r") as file:
        return file.read()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.command()
async def logged_messages(ctx):
    logged_messages = get_logged_messages()
    await ctx.send(logged_messages)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$clearmessagelogs') and message.author.id == CLEAR_ID:
        clear_messages()
        await message.channel.send("Message logs cleared.")
        return

    async with message.channel.typing():
        intro_message = get_intro_message()
        previous_messages = get_logged_messages()
        log_message(message)
        response = model.generate_content(
            f"{intro_message}. And also, the messages the user said before are:\n{previous_messages}\nNow the question is: {message.content}")

        if response.text:
            response_text = response.text
            if len(response_text) <= 2000:
                await message.channel.send(response_text)
            else:
                await message.channel.send(response_text[:2000])
                await message.channel.send(response_text[2000:])
        else:
            await message.channel.send("I'm sorry, I couldn't generate a response.")

client.run(TOKEN)
