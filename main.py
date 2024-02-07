import asyncio
import discord
import datetime
import subprocess, sys

client = discord.Client(intents=discord.Intents.all())
path = "code/"

def get_config(config_text,config_name):
    text1 = config_text[config_text.index(config_name + "="):].replace(config_name + "=","")
    start = text1.index('[') + 1
    end = text1.index(']')
    return text1[start:end]

def load_config():
    f = open("config.txt", "r", encoding="UTF-8")
    config_text = f.read()
    f.close()

    config_text = config_text.replace(" ", "")
    bot_token = get_config(config_text,"BOT_TOKEN")
    run_chanel = get_config(config_text,"RUN_CHANEL_NAME")
    max_embed_text_size = get_config(config_text,"MAX_EMBED_TEXT_SIZE")

    return bot_token,run_chanel,max_embed_text_size

configs = load_config()
BOT_TOKEN = configs[0]
RUN_CHANEL = configs[1]
MAX_EMBED_TEXT_SIZE = int(configs[2])

@client.event
async def on_ready():
    message = "{0.user}".format(client) + "を起動しました。"
    dt_now = datetime.datetime.now()

    print(message)

    embed = discord.Embed(
                title="Debug-log",
                color=0xff1010,
                description="",                
        )
    embed.set_footer(text="Made by hannsi │ " + dt_now.strftime("%Y年%m月%d日 %H:%M:%S"))
    embed.add_field(name="",value=message)

    for channel in client.get_all_channels():
	    if channel.name == RUN_CHANEL:
		    await channel.send(embed=embed)

@client.event
async def on_close():
    message = "{0.user}".format(client) + "を終了させました。"
    dt_now = datetime.datetime.now()

    print(message)

    embed = discord.Embed(
                title="Debug-log",
                color=0xff1010,
                description="",                
        )
    embed.set_footer(text="Made by hannsi │ " + dt_now.strftime("%Y年%m月%d日 %H:%M:%S"))
    embed.add_field(name="",value=message)

    for channel in client.get_all_channels():
	    if channel.name == RUN_CHANEL:
		    await channel.send(embed=embed)

@client.event
async def on_message(message):
    dt_now = datetime.datetime.now()
    if message.author == client.user:
        return
    if message.channel.name != RUN_CHANEL:
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

    result_text = result[0]

    title = "実行結果"

    if(len(result_text) > MAX_EMBED_TEXT_SIZE):
        result_text = result_text[0:MAX_EMBED_TEXT_SIZE]
        title = title + "(文字数制限[" + str(MAX_EMBED_TEXT_SIZE) + "]により一部結果が省かれています。)"

    embed = discord.Embed(
                title=title,
                color=0xff1010,
                description="",                
        )
    embed.set_footer(text="実行者 : " + author + " │ " + dt_now.strftime("%Y年%m月%d日 %H:%M:%S"))
    embed.add_field(name="結果",value=result_text)

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

client.run(BOT_TOKEN)
