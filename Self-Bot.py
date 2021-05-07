import asyncio
import json
import logging
import random
import string
import typing
from datetime import datetime
 
import discord
from discord import Embed, Colour
from discord.ext import commands, tasks
 
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
try:
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
except FileNotFoundError:
    pass
 
 
def open_file(file: str):
    with open(file, "r") as f:
        if file.endswith(".json"):
            return json.load(f)
        return f.read()
 
 
main = True
if main:
    TOKEN = open_file("token.txt").split()[0]
else:
    TOKEN = open_file("token.txt").split()[1]
# USER_IDS = [int(i) for i in open_file("users.txt").split()]
PASSWORD = open_file("password.txt")
 
print("Initialized")
 
 
class SelfBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix="?", case_insensitive=True, self_bot=True)
        self.split = " "
        self.x = 0
        self.statuses = []
        self.status_index = 0
        self.autostatus = False
        self.channels = []
        self.nicknames = {}  # guild_id: [index, [list of nicknames]]
        self.test.start()
        self.msg = "Test"
        # self.troll.start()
        self.change_status.start()
        self.change_nicknames.start()
        self.bet_snakeeyes.start()
        self.dep.start()
        self.postmemes.start()
        self.beg_highlow.start()
        self.work.start()
        self.infrequent.start()
        self.qb_chanid = 0
 
    async def on_ready(self):
        await self.change_presence(status=discord.Status.offline)
        print("Ready")
 
    async def send_embed(self, ctx, string, negative=False, info=False, question=False):
        try:
            string = str(string)
        except Exception as e:
            print(e)
        if negative:
            await ctx.send(embed=Embed(colour=Colour.red(), description=f"{string}"))
        elif info:
            await ctx.send(embed=Embed(colour=Colour.blue(), description=string))
        elif question:
            await ctx.send(embed=Embed(colour=Colour.orange(), description=string))
        else:
            await ctx.send(
                embed=Embed(colour=Colour.green(), description=f"***{string}***"))
 
    # @tasks.loop(minutes=31)
    # async def troll(self):
    #     await self.wait_until_ready()
    #     user = await self.fetch_user(random.choice(USER_IDS))
    #     if user is None:
    #         print(f"Failed to get user: {user}")
    #         return
    #     print(f"Changed (or attempting) to {str(user)}")
    #     url = user.avatar_url_as(format="jpeg")
    #     name = user.name
    #     await self.user.edit(password=PASSWORD, username=name, avatar=await url.read())
 
    @tasks.loop(seconds=10)
    async def test(self):
        await self.wait_until_ready()
        for i in self.channels:
            chan = self.get_channel(i)
            if chan is not None:
                try:
                    await chan.send(self.msg)
                except:
                    pass
 
    @tasks.loop(seconds=5)
    async def change_status(self):
        await self.wait_until_ready()
        try:
            if len(self.statuses) == 0:
                return
            self.status_index += 1
            self.status_index %= len(self.statuses)
            await self.change_presence(activity=discord.Game(self.statuses[self.status_index]))
 
        except Exception as e:
            print(e)
 
    @tasks.loop(seconds=5)
    async def change_nicknames(self):
        await self.wait_until_ready()
        try:
            for guild_id, pair in self.nicknames.items():
                if len(pair[1]) == 0:
                    continue
                member = self.get_guild(guild_id).get_member(self.user.id)
                await member.edit(nick=pair[1][pair[0]])
                pair[0] += 1
                pair[0] %= len(pair[1])
 
        except Exception as e:
            print(e)
 
    async def meme_channel(self):
        await self.wait_until_ready()
        chan_ids = [835869004891160647, 787841828019240981, 820805947236417547]
        for chan_id in chan_ids:
            if self.get_channel(chan_id) is not None:
                chan = self.get_channel(chan_id)
                return chan
 
    @tasks.loop(seconds=11)
    async def bet_snakeeyes(self):
        chan = await self.meme_channel()
        if chan is None:
            print("Dank Memer didn't work")
            return
        await chan.send("pls snakeeyes 10")
        await chan.send("pls bet 10")
 
    @tasks.loop(seconds=6)
    async def dep(self):
        chan = await self.meme_channel()
        if chan is None:
            print("Dank Memer didn't work")
            return
        await chan.send("pls dep all")
 
    @tasks.loop(seconds=41)
    async def postmemes(self):
        chan = await self.meme_channel()
        if chan is None:
            print("Dank Memer didn't work")
            return
        await chan.send("pls postmeme")
        await asyncio.sleep(3)
        await chan.send("f")
 
    @tasks.loop(seconds=46)
    async def beg_highlow(self):
        chan = await self.meme_channel()
        if chan is None:
            print("Dank Memer didn't work")
            return
        await chan.send("pls beg")
        await chan.send("pls highlow")
        await asyncio.sleep(3)
        await chan.send("high")
 
    @tasks.loop(hours=1, seconds=1)
    async def work(self):
        chan = await self.meme_channel()
        if chan is None:
            print("Dank Memer didn't work")
            return
        await chan.send("pls work")
        await asyncio.sleep(3)
        await chan.send("blue")
 
    @tasks.loop(minutes=10)
    async def infrequent(self):
        chan = await self.meme_channel()
        if chan is None:
            print("Dank Memer didn't work")
            return
        await chan.send("pls daily")
 
    @tasks.loop(seconds=3)
    async def trollquotobot(self):
        chan = self.get_channel(self.qb_chanid)
        if chan is None:
            print("Trolling qb didn't work")
            return
        lst = []
        a = string.ascii_lowercase
        for _ in range(100):
            s = ""
            for j in range(4):
                s += random.choice(a)
            lst.append(s)
        await chan.send(f"~spellcheck {' '.join(lst)}")
 
 
bot = SelfBot()
 
 
@bot.command()
async def changestatus(ctx, *, status: str):
    try:
        await bot.change_presence(activity=discord.Game(status))
        await bot.send_embed(ctx, f"Changed presence to {status}")
 
    except Exception as e:
        await bot.send_embed(ctx, str(e), negative=True)
 
 
@bot.command()
async def statuslist(ctx, *, statuses: str):
    """Manually make a changing status with each entry being in the list."""
 
    bot.x = 0
    statuses = statuses.replace("\n", bot.split)
    status_list = statuses.split(bot.split)
    if len(status_list) <= 1:
        return await bot.send_embed(ctx, f"You cannot have a list with only {len(status_list)} entry.", negative=True)
    bot.statuses = status_list
    bot.autostatus = True
    await bot.send_embed(ctx, "Changed statuslist.")
 
 
@bot.command()
async def reversestatusorder(ctx):
    """Reverses status order. If it was going right, it would go left after this command, and vice versa."""
 
    bot.statuses.reverse()
    await bot.send_embed(ctx, "Changed status order.")
 
 
@bot.command()
async def changeseconds(ctx, seconds: int):
    """Number of seconds between changing the status of the bot. Beware, anything below 12 may get the bot rate
    limited."""
 
    if 1 <= seconds <= 120:
        bot.change_status.change_interval(seconds=seconds)
        await bot.send_embed(ctx, f"Successfully changed status changing cooldown to {str(seconds)}")
    else:
        await bot.send_embed(ctx, "Invalid time to change seconds; must be an integer between 1 and 120.",
                             negative=True)
 
 
@bot.command()
async def testseconds(ctx, seconds: int):
    bot.test.change_interval(seconds=seconds)
    await bot.send_embed(ctx, f"Successfully changed status changing cooldown to {str(seconds)}")
 
 
@bot.command()
async def test(ctx, *, s: str):
    bot.msg = s
    await bot.send_embed(ctx, f"Successfully changed test message to {s}.")
 
 
@bot.command()
async def autostatus(ctx, space: typing.Optional[bool] = True, *, status: str):
    """Autostatus the bot. Cycles through the provided name every second just like Aimware.net in CSGO. You might
    get rate limited if you put the number of seconds under 60."""
 
    if space:
        status += " "
 
    try:
        bot.x = 0
        bot.statuses = [status]
        status = list(status)
        for i in range(len(status) - 1):
            lastposition = status.pop()
            status.insert(0, lastposition)
            bot.statuses.append("".join(status))
        bot.autostatus = True
        print(bot.statuses)
        await bot.send_embed(ctx, f"Successfully set autostatus on {bot.statuses[0]}")
 
    except Exception as e:
        await bot.send_embed(ctx, str(e), negative=True)
 
 
@bot.command()
async def changesplit(ctx, split: str):
    """Change the split that the list splits on. For example, say that you want 'a r' in the status changing list,
    but you can't because the list splits on the whitespace. You can change the split to, for example, 'ttg' and it
    won't split on 'a r' anymore. You just have to sub out space for 'ttg'. Another example; if I want a list with
    'duck', 'goose', and 'mouse', with '4' as the split, I can do 'duck4goose4mouse' to get the list. Sub
    out where you would normally put a spacebar for the split. You can make the split as long or short as you want,
    as long as it's not 0 characters. It can even include spaces if you like!."""
 
    bot.split = split
    await bot.send_embed(ctx, f"Split changed to ``{split}``.")
 
 
@bot.command()
async def troll(ctx, user: discord.User):
    await bot.wait_until_ready()
    print(f"Changed (or attempting) to {str(user)}")
    url = user.avatar_url_as(format="jpeg")
    name = user.name
    try:
        await bot.user.edit(password=PASSWORD, username=name, avatar=await url.read())
        await ctx.send(f"Successfully trolled {str(user)}!")
    except discord.HTTPException:
        await ctx.send("You are being rate limited right now. :(")
 
 
@bot.command()
async def purge(ctx, n: int, chan_id: int = None):
    await bot.wait_until_ready()
    if chan_id is None:
        chan = ctx.channel
    else:
        chan = bot.get_channel(chan_id)
    if chan is None:
        await bot.send_embed(ctx, "Invalid channel ID.", negative=True)
        return
    if n > 1000:
        await bot.send_embed(ctx, "Too many messages to delete", negative=True)
        return
    elif n <= 0:
        await bot.send_embed(ctx, "Messages cannot be negative.", negative=True)
        return
    try:
        if isinstance(chan, discord.TextChannel):
            await chan.purge(limit=n, check=lambda x: x.author == bot.user, bulk=False)
        elif isinstance(chan, discord.GroupChannel):
            c = 0
            async for msg in chan.history(limit=1000):
                if c >= n:
                    break
                if msg.author == ctx.author:
                    await msg.delete()
                    c += 1
        await ctx.send(f"Purged {n} messages.", delete_after=10)
    except discord.HTTPException:
        await bot.send_embed(ctx, "Looks like you got rate limited!", negative=True)
 
 
@bot.command()
async def addchannel(ctx, n: int):
    bot.channels.append(n)
    await bot.send_embed(ctx, "Added channel.")
 
 
@bot.command()
async def removechannel(ctx, n: int):
    try:
        bot.channels.remove(n)
        await bot.send_embed(ctx, "Remove channel.")
    except ValueError:
        await bot.send_embed(ctx, "Channel hasn't been added yet.", negative=True)
 
 
@bot.command()
async def spam(ctx, *, string: str):
    print(ctx.guild.channels)
    for chan in ctx.guild.channels:
        try:
            await chan.send(string)
        except:
            pass
 
 
@bot.command()
async def addall(ctx):
    for chan in ctx.guild.channels:
        bot.channels.append(chan.id)
 
 
@bot.command()
async def massdelete(ctx, ID: int = None, limit: int = None):
    import time
    if ID is None:
        ID = ctx.channel.id
    try:
        guild = bot.get_guild(ID) or await bot.fetch_guild(ID)
    except:
        guild = None
    chans = []
    if guild is None:
        chan = bot.get_channel(ID)
        if chan is None:
            await ctx.send("Invalid channel.")
            return
        chans.append(chan)
    else:
        for chan in guild.channels:
            if isinstance(chan, discord.TextChannel):
                chans.append(chan)
    if not chans:
        await ctx.send("No channels in the guild")
        return
    for chan in chans:
        if not chan.permissions_for(ctx.author).read_message_history:
            await ctx.send(f"Could not read message history for: {str(chan)}")
            continue
        else:
            await ctx.send(f"Currently deleting messages in: {str(chan)}")
        c = 0
        async for msg in chan.history(limit=limit):
            if msg.author == ctx.author:
                t = time.time()
                try:
                    await msg.delete()
                    print(f"Deleted message with id {msg.id}, time: {round(time.time() - t, 2)}s")
                except:
                    continue
                c += 1
            if limit is not None and c >= limit:
                break
    await bot.send_embed(ctx, "Done")
 
 
@bot.command(aliases=["memberinfo"])
async def userinfo(ctx, member_id: int = None, guild_id: int = None):
    """Show user info."""
 
    member = bot.get_user(member_id) or await bot.fetch_user(member_id)
    if member_id and not member:
        await bot.send_embed(ctx, f"Could not find member with ID {member_id}", negative=True)
        return
    elif not member:
        member = ctx.author
    if guild_id is None and ctx.guild is None:
        await bot.send_embed(ctx, f"You are not in a guild right now.", negative=True)
        return
    elif guild_id is None:
        guild = ctx.guild
    else:
        guild = bot.get_guild(guild_id) or await bot.fetch_guild(guild_id)
        if guild is None:
            await bot.send_embed(ctx, f"Could not find guild with id {guild_id}", negative=True)
            return
 
    member = guild.get_member(member.id) or await guild.fetch_member(member.id)
    if member is None:
        await bot.send_embed(ctx, f"Could not find member {str(member)} in guild {str(guild)}.", negative=True)
        return
 
    embed = discord.Embed(colour=discord.Colour.blue(), description=member.mention)
    embed.set_author(name=str(member), icon_url=str(member.avatar_url))
    embed.set_thumbnail(url=str(member.avatar_url))
    embed.add_field(name="Joined", value=member.joined_at.strftime('%m/%d/%Y, %H:%M:%S'))
    embed.add_field(name="Registered", value=member.created_at.strftime('%m/%d/%Y, %H:%M:%S'))
    roles = ", ".join([role.name for role in member.roles if role != guild.default_role])
    if not roles:
        roles = "None"
    embed.add_field(name=f"Roles ({len(member.roles) - 1})", value=roles, inline=False)
    permissions = []
    if member.guild_permissions.kick_members:
        permissions.append("Kick Members")
    if member.guild_permissions.ban_members:
        permissions.append("Ban Members")
    if member.guild_permissions.administrator:
        permissions.append("Administrator")
    if member.guild_permissions.manage_channels:
        permissions.append("Manage Channels")
    if member.guild_permissions.manage_guild:
        permissions.append("Manage Server")
    if member.guild_permissions.view_audit_log:
        permissions.append("View Audit Log")
    if member.guild_permissions.manage_messages:
        permissions.append("Manage Messages")
    if member.guild_permissions.mention_everyone:
        permissions.append("Mention Everyone")
    if member.guild_permissions.mute_members:
        permissions.append("Mute Members")
    if member.guild_permissions.deafen_members:
        permissions.append("Deafen Members")
    if member.guild_permissions.move_members:
        permissions.append("Move Members")
    if member.guild_permissions.manage_nicknames:
        permissions.append("Manage Nicknames")
    if member.guild_permissions.manage_roles:
        permissions.append("Manage Roles")
    if member.guild_permissions.manage_webhooks:
        permissions.append("Manage Webhooks")
    if member.guild_permissions.manage_emojis:
        permissions.append("Manage Emojis")
    if member.guild_permissions.send_tts_messages:
        permissions.append("Send TTS Messages")
    key_permissions = ", ".join(permissions)
    if not key_permissions:
        key_permissions = "None"
    embed.add_field(name="Key Permissions", value=key_permissions, inline=False)
 
    if member == guild.owner:
        embed.add_field(name="Acknowledgments", value="Server Owner", inline=False)
 
    embed.set_footer(text=f"ID: {member.id}\n"
                          f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
 
    await ctx.send(embed=embed)
 
 
@bot.command()
async def guildinfo(ctx, guild_id: int = None):
    if guild_id is None:
        if ctx.guild is None:
            await bot.send_embed(ctx, "Current channel is not in a guild.", negative=True)
            return
        guild_id = ctx.guild.id
    guild = bot.get_guild(guild_id) or await bot.fetch_guild(guild_id)
    if guild is None:
        await bot.send_embed(ctx, "Invalid guild id.", negative=True)
        return
 
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"{guild.name} statistics",
        description=guild.description
    )
 
    embed.set_thumbnail(url=str(guild.icon_url))
    embed.set_footer(text=f"Created at {guild.created_at.strftime('%m/%d/%Y, %H:%M:%S')}")
 
    value = guild.features
    if not value:
        value = ["None"]
 
    embed.add_field(name="Features", value="\n".join(value))
 
    lockedtextchannels = 0
    lockedcategorychannels = 0
 
    if not guild.default_role.permissions.view_channel:
        lockedtextchannels = len(guild.text_channels)
        lockedcategorychannels = len(guild.categories)
 
    else:
        for chan in guild.text_channels:
            if chan.overwrites_for(guild.default_role).view_channel is False:
                lockedtextchannels += 1
 
        for category in guild.categories:
            if category.overwrites_for(guild.default_role).view_channel is False:
                lockedcategorychannels += 1
 
    lockedvoicechannels = 0
 
    if not guild.default_role.permissions.connect:
        lockedvoicechannels = len(guild.voice_channels)
 
    else:
        for chan in guild.voice_channels:
            if chan.overwrites_for(guild.default_role).connect is False:
                lockedvoicechannels += 1
 
    value = f"{len(guild.text_channels)} " \
            f"({lockedtextchannels} locked)\n" + "\n".join(str(i) for i in guild.text_channels
                                                           if not i.category or "ticket" not in i.category.name.lower())
 
    embed.add_field(name="Text channels", value=value, inline=False)
 
    value = f"{len(guild.voice_channels)} " \
            f"({lockedvoicechannels} locked)\n" + "\n".join(str(i) for i in guild.voice_channels)
 
    embed.add_field(name="Voice channels", value=value, inline=False)
 
    value = f"{len(guild.categories)} " \
            f"({lockedcategorychannels} locked)\n" + "\n".join(str(i) for i in guild.categories)
 
    embed.add_field(name="Categories", value=value, inline=False)
 
    online = 0
    idle = 0
    dnd = 0
    streaming = 0
    offline = 0
    bots = 0
 
    for i in guild.members:
        if i.status.value == "online":
            online += 1
        elif i.status.value == "idle":
            idle += 1
        elif i.status.value == "dnd":
            dnd += 1
        elif i.status.value == "offline":
            offline += 1
        if i.bot:
            bots += 1
        if isinstance(i.activity, discord.Streaming):
            streaming += 1
 
    value = f"Online: {online}\n" \
            f"Idle: {idle}\n" \
            f"Do not disturb: {dnd}\n" \
            f"Streaming: {streaming}\n" \
            f"Offline: {offline}\n" \
            f"Total: {len(guild.members)} members ({bots} bots)"
 
    embed.add_field(name="Members", value=value, inline=False)
 
    value = f"Nitro Tier: {guild.premium_tier}\n" \
            f"Boosters: {guild.premium_subscription_count}\n" \
            f"Maximum bitrate: {int(guild.bitrate_limit)} hz\n" \
            f"File size limit: {int(guild.filesize_limit / 1048576)}MB\n" \
            f"Maximum number of emojis: {guild.emoji_limit}"
 
    embed.add_field(name="Nitro", value=value, inline=False)
 
    value = f"{len(guild.roles)} roles, of which " \
            f"{len([i for i in guild.roles if i.permissions.administrator])} have administrator permissions."
 
    embed.add_field(name="Roles", value=value, inline=False)
 
    animated = len([i for i in guild.emojis if i.animated])
 
    value = f"Regular: {len(guild.emojis) - animated}/{guild.emoji_limit}\n" \
            f"Animated: {animated}/{guild.emoji_limit}\n" \
            f"{len(guild.emojis)}/{guild.emoji_limit} total"
 
    embed.add_field(name="Emojis", value=value, inline=False)
 
    if not guild.afk_channel:
        afkchannel = "None"
    else:
        afkchannel = f"<#{guild.afk_channel.id}>"
 
    #f"Owner: {guild.owner.mention}\n"
    value = f"ID: {guild.id}\n" \
            f"AFK Timeout: {int(guild.afk_timeout / 60)} minutes\n" \
            f"AFK Channel: {afkchannel}\n" \
            f"Voice Region: {guild.region if isinstance(guild.region, str) else guild.region.value}\n" \
            f"Icon URL: {str(guild.icon_url) if str(guild.icon_url) else 'None'}\n" \
            f"Banner URL: {str(guild.banner_url) if str(guild.banner_url) else 'None'}\n"
 
    embed.add_field(name="Miscallenous", value=value, inline=False)
 
    await ctx.send(embed=embed)
 
 
@bot.command()
async def nicktime(ctx, seconds: int):
    bot.change_nicknames.change_interval(seconds=seconds)
    await bot.send_embed(ctx, f"Changed interval to {seconds} seconds.")
 
 
@bot.command()
async def changenick(ctx, guild_id: int, *, string: str = None):
    if string is None:
        del bot.nicknames[guild_id]
        await bot.send_embed(ctx, f"Successfully removed nicknames for server {bot.get_guild(guild_id).name}.")
        return
    string = string.replace("\n", bot.split)
    lst = string.split(bot.split)
    bot.nicknames[guild_id] = [0, lst]
    try:
        await bot.send_embed(ctx, f"Changed nicknames for server {bot.get_guild(guild_id).name}.")
    except Exception as e:
        await bot.send_embed(ctx, str(e), negative=True)
 
 
@bot.command()
async def startdankmemer(ctx):
    bot.change_status.start()
    bot.change_nicknames.start()
    bot.bet_snakeeyes.start()
    bot.dep.start()
    bot.postmemes.start()
    bot.beg_highlow.start()
    bot.work.start()
    bot.infrequent.start()
    await bot.send_embed(ctx, "Started dank memer selfbot.")
 
 
@bot.command()
async def enddankmemer(ctx):
    bot.change_status.stop()
    bot.change_nicknames.stop()
    bot.bet_snakeeyes.stop()
    bot.dep.stop()
    bot.postmemes.stop()
    bot.beg_highlow.stop()
    bot.work.stop()
    bot.infrequent.stop()
    await bot.send_embed(ctx, "Stopped dank memer selfbot.", negative=True)
 
 
@bot.command()
async def startquotobot(ctx):
    bot.qb_chanid = ctx.channel.id
    bot.trollquotobot.start()
    await bot.send_embed(ctx, "Started trolling QB.")
 
 
@bot.command()
async def endquotobot(ctx):
    bot.trollquotobot.stop()
    await bot.send_embed(ctx, "Stopped trolling QB.")
 
 
@bot.command()
async def emote(ctx, channel_id: int, *, text: str):
    chan = bot.get_channel(channel_id)
    if chan is None:
        return await bot.send_embed(ctx, "Channel not found.", negative=True)
    d = {
        "a": "🇦",
        "b": "🇧",
        "c": "🇨",
        "d": "🇩",
        "e": "🇪",
        "f": "🇫",
        "g": "🇬",
        "h": "🇭",
        "i": "🇮",
        "j": "🇯",
        "k": "🇰",
        "l": "🇱",
        "m": "🇲",
        "n": "🇳",
        "o": "🇴",
        "p": "🇵",
        "q": "🇶",
        "r": "🇷",
        "s": "🇸",
        "t": "🇹",
        "u": "🇺",
        "v": "🇻",
        "w": "🇼",
        "x": "🇽",
        "y": "🇾",
        "z": "🇿",
        "0": "0️⃣",
        "1": "1️⃣",
        "2": "2️⃣",
        "3": "3️⃣",
        "4": "4️⃣",
        "5": "5️⃣",
        "6": "6️⃣",
        "7": "7️⃣",
        "8": "8️⃣",
        "9": "9️⃣"
    }
    lst = []
    for i, v in d.items():
        lst.append((i.upper(), v))
    for i in lst:
        d[i[0]] = i[1]
    s = " ".join(d[i] if i in d else i for i in text)
    await chan.send(s)
    await bot.send_embed(ctx, "Sent text.")
 
bot.run(TOKEN, bot=False)