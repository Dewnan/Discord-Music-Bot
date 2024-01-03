import discord
from discord.ext import commands
import youtube_dl
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from the environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!')

# Dictionary to store the voice clients for each server
voice_clients = {}

@bot.event
async def on_ready():
    print("Bot Online...")

@bot.command(name='join', help='Join the voice channel')
async def join(ctx):
    channel = ctx.author.voice.channel
    voice_clients[ctx.guild.id] = await channel.connect()

@bot.command(name='leave', help='Leave the voice channel')
async def leave(ctx):
    voice_client = voice_clients.get(ctx.guild.id)
    if voice_client:
        await voice_client.disconnect()
        del voice_clients[ctx.guild.id]

@bot.command(name='play', help='Play a song from YouTube')
async def play(ctx, url):
    voice_client = voice_clients.get(ctx.guild.id)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']

    voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))

@bot.command(name='skip', help='Skip the current song')
async def skip(ctx):
    voice_client = voice_clients.get(ctx.guild.id)
    if voice_client.is_playing():
        voice_client.stop()

bot.run(BOT_TOKEN)
