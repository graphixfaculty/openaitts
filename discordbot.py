import discord
from discord.ext import commands
from os import getenv
import openai
import traceback

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
openai.api_key = getenv('OPENAI_API_KEY')  # APIキーを初期化

@bot.event
async def on_command_error(ctx, error):
    error_msg = "An error occurred. Please try again later."
    await ctx.send(error_msg)
    print(''.join(traceback.TracebackException.from_exception(error).format()))  # ログ出力

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        user_id = message.author.id
        if user_id not in messages:
            messages[user_id] = []
        content = message.content.replace(message.guild.me.mention, '').strip()
        messages[user_id].append({"role": "user", "content": content})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages[user_id]
        )

        reply = completion.choices[0].message['content']
        await message.channel.send(reply)
        messages[user_id].append({"role": "assistant", "content": reply})

bot.run(getenv('DISCORD_BOT_TOKEN'))
