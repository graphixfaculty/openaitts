# OpenAI_Bot.py
import os

import discord
import openai


from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = discord.Client(intents=discord.Intents.all())

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("OpenAIBot is in " + str(guild_count) + " guilds.")


# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
    # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
    if message.content.find('AI!') != -1:

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=message.content[3:],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        await message.channel.send(response["choices"][0]["text"])

bot.run(DISCORD_TOKEN)
# EXECUTES THE BOT WITH THE SPECIFIED DISCORD_TOKEN. DISCORD_TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
