import asyncio
import discord
import datetime
import subprocess, sys

def load_config():
    f = open("config.txt", "r", encoding="UTF-8")
    config_text = f.read()
    print("test:" + config_text)
    f.close()

    bot_token_text = config_text.replace(" ", "")
    d_index = bot_token_text.index("BOT_TOKEN=")
    TOKEN = bot_token_text[d_index:].replace("BOT_TOKEN=","")

    return TOKEN

TOKEN = load_config()
client = discord.Client(intents=discord.Intents.all())
path = "code/"

@client.event
async def on_ready():
    message = "{0.user}".format(client) + "としてログインしました。"
    dt_now = datetime.datetime.now()

    print(message)

    embed = discord.Embed(
                title="Debug-log",
                color=0xff1010,
                description="",                
        )
    embed.set_footer(text="Made by hannsi │ " + dt_now.strftime("%Y年%m月%d日 %H:%M:%S"))
    embed.add_field(name="",value=message)

    ch_name = "実行"

    for channel in client.get_all_channels():
	    if channel.name == ch_name:
		    await channel.send(embed=embed)

@client.event
async def on_close():
    message = "{0.user}".format(client) + "はログアウトしました。"
    dt_now = datetime.datetime.now()

    print(message)

    embed = discord.Embed(
                title="Debug-log",
                color=0xff1010,
                description="",                
        )
    embed.set_footer(text="Made by hannsi │ " + dt_now.strftime("%Y年%m月%d日 %H:%M:%S"))
    embed.add_field(name="",value=message)

    ch_name = "実行"

    for channel in client.get_all_channels():
	    if channel.name == ch_name:
		    await channel.send(embed=embed)

@client.event
async def on_message(message):
    dt_now = datetime.datetime.now()
    if message.author == client.user:
        return

    code = message.content
    author = str(message.author)

    print(author + " : " + code)
    create_python_file(author,code)
    result = run_python_file(author)

    error = result[1]
    r = "No Error"

    if result[2] == 1:
        r = error

    embed = discord.Embed(
                title="実行結果",
                color=0xff1010,
                description="",                
        )
    embed.set_footer(text="実行者 : " + author + " │ " + dt_now.strftime("%Y年%m月%d日 %H:%M:%S"))
    embed.add_field(name="結果",value=result[0])
    if result[2] == 1:
        embed.add_field(name="エラー",value=r)

    await message.channel.send(embed=embed)

def create_python_file(file_name,code):
    f = open(path + file_name + ".py", "w", encoding='UTF-8')
    f.write(code)
    f.close()

def run_python_file(file_name):
    try:
        cp = subprocess.run(["python", path + file_name + ".py"], encoding='CP932', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(cp.returncode)
        print('stdout:' + cp.stdout)
        print('stderr:' + cp.stderr)
        print("return code:" + str(cp.returncode))
    except subprocess.CalledProcessError as cpe:
        print('returncode:' + str(cpe.returncode))
        print('stderr:'     + cpe.stderr)
        print('cmd:'        + cpe.cmd)
        raise cpe
    
    return cp.stdout,cp.stderr,cp.returncode

client.run(TOKEN)
