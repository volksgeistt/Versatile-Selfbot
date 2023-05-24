import discord
from discord.ext import commands
import requests
from colorama import Fore
import os
import pyfiglet
import random
os.system("pip install PyNaCl")

prefix = "~" # Input Your Prefix
client = commands.Bot(command_prefix=prefix,case_insensitive=True,self_bot=True)
client.remove_command('help')
token = " " # Input Your Token
author = "volksgeist#1337"

versatile = pyfiglet.figlet_format(f"VERSATILE")
print(versatile+f"\nMade By {author}\n")

@client.event
async def on_ready():
  print(f"{Fore.GREEN}[!] Connected @ {client.user}")
  print(f"{Fore.RED}[!] Total Cmds: {len(client.commands)}")

 #cmd Error msgs
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f"> ❌ You're Missing Some Arguments, Usage ~ `{ctx.command} {ctx.command.signature}`")
  elif isinstance(error, commands.MissingPermissions):
    await ctx.reply(f"> ❌ Your Are Lacking Perms To Use This Command")
  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.reply(f"> ❌ That Command Is On CoolDown, Try Again After {error.retry_after:.2f} Seconds")
  elif isinstance(error, commands.CommandNotFound):
    await ctx.reply(f"> ❌ No Such Command Found In The SelfBot")
  elif isinstance(error, commands.UserInputError):
    await ctx.reply(f"> ❌ Your Input Is Invalid")

# S 3 L F B O T : I N P U T S
i2c_rate = 90 #input your i2c rate
c2i_rate = 90 #input your c2i rate
ltc_addy = "#" #input your ltc addy
upi_id = "#" #input your upi id
upi_qr = "#" #input your qr img link
twitch_url = "https://twitch.tv/volksgeist"

@client.command(pass_context=True)
@commands.cooldown(1, 4, commands.BucketType.user)
async def help(ctx):
  await ctx.reply(f">>> **V E R S A T I L E : By @{author}**\n\n**__Commands__**\nping, boosts, ltc, qr, upi, calc, i2c, c2i, ltcprice, userinfo, serverinfo, getbal, randomip, ipinfo, joinvc, gayrate, stream, play, watch, listen")


###################################
@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def ltc(ctx):
    await ctx.reply(f"> {ltc_addy}")

@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def upi(ctx):
    await ctx.reply(f"> {upi_id}")

@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def qr(ctx):
    await ctx.reply(f"> {qr}")
  
@client.command(aliases=["calc","solve"])
async def calculate(ctx, *, expression):
    result = eval(expression)
    await ctx.reply(f"> Solved Answer: {result}")

@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def ping(ctx):
    await ctx.reply(f"> Ping: {int(client.latency*1000)}ms")

@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def boosts(ctx):
    await ctx.reply(f"> This Server Has {ctx.guild.premium_subscription_count} Boosts")

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def i2c(ctx, amount: str):
  amount = float(amount.replace('₹', ''))
  usd_amount = amount / i2c_rate
  await ctx.reply(f"> Given Amount Is Equivalent To ${usd_amount:.2f}")

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def c2i(ctx, amount: str):
  amount = float(amount.replace('$', ''))
  usd_amount = amount * c2i_rate
  await ctx.reply(f"> Given Amount Is Equivalent To ₹{usd_amount:.2f}")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def randomip(ctx):
    octets = [random.randint(0, 255) for forgesb in range(4)]
    forgeip = ".".join(map(str, octets))
    await ctx.reply(f"> Random IP: {forgeip}")

@client.command(aliases=["ip-info"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def ipinfo(ctx, ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url).json()
    if response["status"] == "fail":
        await ctx.reply(f"> ❌ Invalid IP Address")
        return
    await ctx.reply(f">>> **IP Address:** {response['query']}\n**Location:** {response['city']}, {response['regionName']}, {response['country']}\n**ISP:** {response['isp']}\n**Organization:** {response['org']}\n**Timezone:** {response['timezone']}")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def gayrate(ctx, User: discord.Member=None):
   if User is None:
    await ctx.reply(f"> ❌ You Didn't Provide Any User")
   else:
    await ctx.reply(f"> {User.mention} Is {random.randrange(101)}% Gay")

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def joinvc(ctx, vc_id: int):
    voice_channel = client.get_channel(vc_id)
    if not voice_channel or not isinstance(voice_channel, discord.VoiceChannel):
        await ctx.reply('> ❌ Invalid Channel ID')
        return
    try:
        voice_client = await voice_channel.connect()
        await ctx.reply(f'> ✅ Joined VC ~ #{voice_channel.name}.')
    except discord.DiscordException as e:
        await ctx.reply(f'> ❌ Error Occured While Joining The VC #{e}')

@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def ltcprice(ctx):
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd")
        data = response.json()
        if "litecoin" in data:
            ltc_price = data["litecoin"]["usd"]
            await ctx.reply(f"> 🪙 Current LTC Pricing: ${ltc_price:.2f}")
        else:
            await ctx.reply("> ❌ Unable To Fetch LTC Price")
    except requests.RequestException:
        await ctx.reply("> ❌ An Error Occured While Requesting LTC Price")


@client.command(aliases=["ui","uinfo"])
@commands.cooldown(1, 4, commands.BucketType.user)
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    roles = [role.name for role in member.roles[1:]] 
    roles_str = ', @'.join(roles) if roles else 'None'
    created_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
    joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
    user_info = (f">>> **__UserInfo Statistics For {member.mention}__**\n\n**Username:** {member.name}\n**Discriminator:** #{member.discriminator}\n**User ID:** {member.id}\n**Created At:** {created_at}\n**Joined At:** {joined_at}\n**Roles:** {roles_str}")
    await ctx.send(user_info)

@client.command(aliases=["si","sinfo"])
async def serverinfo(ctx):
    server = ctx.guild
    server_name = server.name
    server_id = server.id
    server_owner = server.owner
    server_region = server.region
    member_count = server.member_count
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    total_cnl = text_channels + voice_channels
    server_created_at = server.created_at.strftime("%Y-%m-%d %H:%M:%S")
    server_info = (f">>> **__ServerInfo Statistics: {server_name}__**\n\n**Server Name:** {server_name}\n**Server ID:** {server_id}\n**Server Owner:** {server_owner}\n**Server Region:** {server_region}\n**MemberCount:** {member_count}\n**Text Channels:** {text_channels}\n**Voice Channels:** {voice_channels}\n**Total Channels:**  {total_cnl}\n**Created At:** {server_created_at}")
    await ctx.send(server_info)

@client.command()
async def spam(ctx, amount: int, *, message: str):
    for codeforge in range(amount):
        await ctx.send(message)

@client.command()
async def stream(ctx, *, message):
    stream = discord.Streaming(name=message,url=twitch_url)
    await client.change_presence(activity=stream)
    await ctx.reply("> Changed Your Activity Status As Streaming!")

@client.command()
async def play(ctx, *, message):
    game = discord.Game(name=message) 
    await client.change_presence(activity=game) 
    await ctx.reply("> Changed Your Activity Status As Playing!")

@client.command()
async def watch(ctx, *, message):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))
    await ctx.reply("> Changed Your Activity Status As Watching!")

@client.command()
async def listen(ctx, *, message):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=message))
    await ctx.reply("> Changed Your Activity Status As Listening!")

#Outsider cmds
@client.command()
async def getbal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
    balance = response.json()['final_balance'] / 10**8
    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    usd_price = cg_response.json()['litecoin']['usd']
    usd_balance = balance * usd_price
    message=f"> 💵 Balance: {usd_balance:.2f}"
    await ctx.send(message)

client.run(token,bot=False)
