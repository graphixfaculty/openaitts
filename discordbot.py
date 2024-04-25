import discord
from discord.ext import commands
from discord.ext.commands import Context
from os import getenv
#import openai
from openai import OpenAI
import traceback
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

#openai.api_key = getenv('OPENAI_API_KEY')
apikey = getenv('OPENAI_API_KEY')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_command_error(ctx: Context, error):
    await ctx.send('An unexpected error occurred. Please try again.')
    print('Error occurred:', traceback.format_exception_only(type(error), error))

@bot.command(name='join')
async def join(ctx):
    """Joins a voice channel"""
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()

@bot.command(name='leave')
async def leave(ctx):
    """Leaves a voice channel"""
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        user_msg = message.content.replace(f'<@{bot.user.id}>', '').strip()
        print(user_msg)

        try:
            # Generate voice from text
            client = OpenAI(api_key=apikey)
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=user_msg
            )
            
            # Save audio to a file
            audio_data = response.read()
            with open('response.mp3', 'wb') as audio_file:
                audio_file.write(audio_data)
                #audio_file.write(response['audio'])
            
            with open('response.mp3', 'rb') as audio_file:
                await message.channel.send(file=discord.File(audio_file, 'response.mp3'))

        except Exception as e:
            error_details = f"Error: {str(e)}"
            print(error_details)
            await message.channel.send(error_details)

bot.run(getenv('DISCORD_BOT_TOKEN'))
