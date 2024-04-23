import discord
from discord.ext import commands
from os import getenv
import openai
import traceback

intents = discord.Intents.default()
intents.message_content = True  # Need this intent to read message content
bot = commands.Bot(command_prefix='/', intents=intents)

# Set up OpenAI key once
openai.api_key = getenv('OPENAI_API_KEY')

messages = [
    {"role": "system", "content": "You are a helpful assistant. The AI assistant's name is AI Qiitan."},
    {"role": "user", "content": "こんにちは。あなたは誰ですか？"},
    {"role": "assistant", "content": "私は AI アシスタントの AI Qiitan です。なにかお手伝いできることはありますか？"}
]

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = 'An unexpected error occurred. Please try again.'
    await ctx.send(error_msg)
    # Logging the error
    print(''.join(traceback.TracebackException.from_exception(orig_error).format()))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Handling mentions properly
    if bot.user in message.mentions:
        user_msg = message.content.replace(f'<@{bot.user.id}>', '').strip()
        print(user_msg)
        messages.append({"role": "user", "content": user_msg})

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            bot_response = completion.choices[0].message['content']
            print(bot_response)
            await message.channel.send(bot_response)
        except Exception as e:
            await message.channel.send("Error processing your request, please try again.")
            print(e)

bot.run(getenv('DISCORD_BOT_TOKEN'))
