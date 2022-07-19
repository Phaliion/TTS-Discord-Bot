import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import *
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
#from keep_alive import keep_alive
import gtts
from gtts import gTTS

client = commands.Bot(command_prefix=".")
client.remove_command('help')
DiscordComponents(client)

@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(status=discord.Status.idle, activity=Game(name=f'on {len(client.guilds)} servers | .help'))
    #client.loop.create_task(loop())

@client.command()
async def help(ctx):
    with open(r"Data/accent.txt","r") as f: lines = f.readlines()
    for line in lines:
        if line.split(",")[0] == str(ctx.guild.id):
            if line.split(",")[1] != "com":
                accent=(line.split(",")[1].replace("com.","").replace("co.","")).upper()
            else:
                accent="US"
    embed = discord.Embed(title="Help:")
    embed.add_field(name="TTS: ", value=".tts <$say-name['true']> <message>")
    embed.add_field(name="Leave Voice:", value=".leave")
    embed.add_field(name="Change Accent:", value=f".accent <accent> \n(leave <accent> feild blank for list)\n> Current Accent: {accent}",inline=False)
    embed.set_footer(text="$: Optional\n[]: options\nLatency: {0}ms".format(round(client.latency, 4)*1000))
    await ctx.send(embed=embed)


@client.command()
async def tts(ctx, say_name : str=None, *, text=""):
    if say_name.title() == 'True' or say_name.title() == 'False':
        if say_name.title() == 'False':
            mytext = text
        else:
            mytext = f"{str(ctx.author).split('#')[0]} says, {text}"
    else:
        mytext = f"{say_name} {text}"

    # text to speech
    with open(r"Data/accent.txt","r") as f:
        lines = f.readlines()
    accent=False
    for line in lines:
        if line.split(",")[0] == str(ctx.guild.id):
            accent=line.split(",")[1].strip("\n")
    if accent==False: accent="com"
    language = 'en'
    myobj = gTTS(text=mytext, tld=accent, lang=language, slow=False)
    myobj.save("file.mp3")

    # joins channel and play it
    channel = ctx.author.voice
    try:
        channel = str(channel).split("name=")[1].split(" rtc_region=")[0].replace("'","")
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice == None:
            await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("file.mp3"))
        embed = discord.Embed(title="Playing message...")
        embed.add_field(name="Message:",value=mytext)
    except:
        embed = discord.Embed(title="Must be in a voice channel.")
    embed.set_footer(text="Latency: {0}ms".format(round(client.latency, 4)*1000))
    await ctx.send(embed=embed)

@client.command(aliases=['acent'])
async def accent(ctx, *, accent : str=None):
    if accent == None:
        embed = discord.Embed(title="Must input a accent.", description="Ex: .accent uk")
        embed.add_field(name="Accents: ", value="Australian: au\nUnited Kingdom: uk\nUnited Stated: us\nCanada: ca\nIndia: in\nIreland: ie\nSouth Africa: za\nFrance: fr\nBrazil: br\nPortugal: pt\nMexico: mx\nSpain: es")
        embed.set_footer(text="Latency: {0}ms".format(round(client.latency, 4)*1000))
        await ctx.send(embed=embed)
    else:
        if accent.lower() == 'au' or accent.lower() == 'us' or accent.lower() == 'br' or accent.lower() == 'mx':
            if accent.lower() == "us":
                decision='com'
            else:
                decision=f"com.{accent}"
        elif accent.lower() == 'uk' or accent.lower() == 'in' or accent.lower() == 'za':
            decision=f"co.{accent}"
        else:
            if accent.lower() != 'ca' or accent.lower() != 'ie' or accent.lower() != 'fr' or accent.lower() != 'pt' or accent.lower() != 'es':
                embed = discord.Embed(title="Must input a valid accent.", description="Ex: .accent uk")
                embed.add_field(name="Accents: ", value="Australian: au\nUnited Kingdom: uk\nUnited Stated: us\nCanada: ca\nIndia: in\nIreland: ie\nSouth Africa: za\nFrance: fr\nBrazil: br\nPortugal: pt\nMexico: mx\nSpain: es")
                embed.set_footer(text="Latency: {0}ms".format(round(client.latency, 4)*1000))
                await ctx.send(embed=embed)
                decision=False
            else:
                decision=accent

        with open(r"Data/accent.txt","r") as f:
            lines = f.readlines()
        data = open(r"Data/accent.txt","w")
        temp=False
        for line in lines:
            if line!="\n" and line.split(",")[0] != str(ctx.guild.id):
                try:
                    if line.split(",")[1] != "TrueFalse":
                        data.write(f"{line}\n")
                except Exception as e: print(e)
            else:
                lint=line
        if decision != False:
            data.write(f"{str(ctx.guild.id)},{decision}\n")
            embed = discord.Embed(title="Accent Set Successfully.", description=f"Set to {accent.upper()}.")
            embed.set_footer(text="Latency: {0}ms".format(round(client.latency, 4)*1000))
            await ctx.send(embed=embed)
        else:
            data.write(lint)
        data.close()


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        await voice.disconnect()
        embed= discord.Embed(title="Disconnected from Voice.")
    except:
        embed = discord.Embed(title="The bot is not connected to a voice channel")
    embed.set_footer(text="Latency: {0}ms".format(round(client.latency, 4)*1000))
    await ctx.send(embed=embed)

client.run("TOKEN")