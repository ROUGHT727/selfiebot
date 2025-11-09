import os
import discord
from discord.ext import commands

# Enable all intents
intents = discord.Intents.all()

# Initialize self-bot
bot = commands.Bot(
    command_prefix='?',
    self_bot=True,
    help_command=None,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'🤖 Logged in as {bot.user} (ID: {bot.user.id})')
    print('✅ Self-bot is running.')

# ===========================
# Commands
# ===========================

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    if amount <= 0:
        return await ctx.send("Please specify a number > 0.", delete_after=5)
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'**{len(deleted)-1}** messages purged.', delete_after=5)
    except discord.Forbidden:
        await ctx.send("Need permission to manage messages.", delete_after=5)

@bot.command()
async def edit(ctx, *, new_content):
    await ctx.message.delete()
    async for msg in ctx.channel.history(limit=5):
        if msg.author.id == bot.user.id:
            await msg.edit(content=new_content)
            return
    await ctx.send("No recent message to edit.", delete_after=5)

@bot.command()
async def nick(ctx, *, new_nick=None):
    await ctx.message.delete()
    if not ctx.guild:
        return await ctx.send("This command works in servers only.", delete_after=5)
    member = ctx.guild.me
    try:
        await member.edit(nick=new_nick)
        msg = f"Nickname changed to **{new_nick}**." if new_nick else "Nickname cleared."
        await ctx.send(msg, delete_after=5)
    except discord.Forbidden:
        await ctx.send("Cannot change nickname (no permission).", delete_after=5)

@bot.command()
async def status(ctx, status_type, *, activity_name=None):
    await ctx.message.delete()
    status_map = {
        'online': discord.Status.online,
        'idle': discord.Status.idle,
        'dnd': discord.Status.dnd,
        'invisible': discord.Status.invisible
    }
    new_status = status_map.get(status_type.lower())
    if not new_status:
        return await ctx.send("Invalid status. Use: online/idle/dnd/invisible.", delete_after=5)
    activity = discord.Game(name=activity_name) if activity_name else None
    await bot.change_presence(status=new_status, activity=activity)

# ===========================
# Run Bot
# ===========================

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise Exception("❌ TOKEN environment variable not found.")
bot.run(TOKEN)
