import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='^', intents=intents)

# Example crop data
crop_data = {
    "carrot": {"time": "10m", "rarity": "common"},
    "goldenrose": {"time": "1h", "rarity": "legendary"},
}

mutation_data = {
    "carrot": ["goldencarrot", "giantcarrot"],
    "rose": ["goldenrose", "blackrose"]
}

active_reminders = {}
user_mutations = {}
trade_offers = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def crop(ctx, name: str):
    crop = crop_data.get(name.lower())
    if crop:
        embed = discord.Embed(title=f"۶<:b08or:1375503529799843850> ˖  __crop__ : {name.capitalize()}", color=0xddbc7e)
        embed.add_field(name="> growth time", value=crop['time'])
        embed.add_field(name="> rarity", value=crop['rarity'])
        await ctx.send(embed=embed)
    else:
        await ctx.send("⚠️ crop not found")

@bot.command()
async def mutation(ctx, crop: str):
    mutations = mutation_data.get(crop.lower())
    if mutations:
        embed = discord.Embed(title=f"۶<:i06bk:1373336226119286914> ˖  __mutations for__ : ˚ {crop.capitalize()} ˖", description="\n".join(mutations), color=0x242424)
        await ctx.send(embed=embed)
    else:
        await ctx.send("⚠️ no mutation data found")

@bot.command()
async def guide(ctx):
    embed = discord.Embed(description="_ _\n_ _    welcome  to  **xinyu’s  garden**\n_ _    ۶<:d01gr:1373340182325235824> g__uide__  for  starters 𓈒\n\n_ _  `  01  `  <:e02bl:1373336216308547725> ₊   𓏲\n_ _   — buy  seeds  to  plant  in  your  pot\n\n_ _  `  02  `  <:c02ye:1373340007347130528> ₊   𓏲\n_ _   —  combine  crops  to  make  mutations\n\n_ _  `  03  `  <:a08re:1375497934107574283> ₊   𓏲\n_ _   —  collect  fully  grown  crops  to  sell\n_ _     or  mutate\n_ _", color=0xFFFFFF)
    await ctx.send(embed=embed)

@bot.command()
async def remind(ctx, crop: str, minutes: int):
    if crop.lower() not in crop_data:
        await ctx.send("⚠️ crop not recognized")
        return

    remind_time = datetime.utcnow() + timedelta(minutes=minutes)
    if ctx.author.id not in active_reminders:
        active_reminders[ctx.author.id] = []
    active_reminders[ctx.author.id].append((crop, remind_time))

    await ctx.send(f"_ _\n_ _    ۶<:e04bl:1375478421915963392> ˖  __reminder set__ :\n_ _    ˚ for {crop} in {minutes} minutes ˖\n_ _")
    await asyncio.sleep(minutes * 60)
    await ctx.send(f"_ _\n_ _    𓈒 harvest ready! {ctx.author.mention} ⁺\n_ _     <:d05gr:1373336210482925639> come check {crop}\n_ _")

@bot.command()
async def mutations_track(ctx, mutation: str):
    if ctx.author.id not in user_mutations:
        user_mutations[ctx.author.id] = []
    user_mutations[ctx.author.id].append(mutation)
    await ctx.send(f"_ _\n_ _    𓈒 mutation {mutation} tracked ⁺\n_ _     <:c08ye:1375501539870773318> for : {ctx.author.name}\n_ _")

@bot.command()
async def mutations_list(ctx):
    mutations = user_mutations.get(ctx.author.id, [])
    if not mutations:
        await ctx.send("⚠️ no mutations tracked yet")
    else:
        embed = discord.Embed(description="_ _\n_ _    𓈒 tracked {mutation} ⁺\n_ _     <:a06re:1373336205474926613> for : {ctx.author.name}\n_ _", color=0xFF5C5C)
        await ctx.send(embed=embed)

@bot.command()
async def trade(ctx, *, offer: str):
    trade_offers.append((ctx.author.name, offer))
    embed = discord.Embed(title="_ _    ۶<:i02bk:1373339853328224406> ˖  __new trade offer__ :", description=offer, color=0x242424)
    embed.set_footer(text=f"˚ㅤofferedㅤbyㅤ{ctx.author.name}ㅤ˖")
    await ctx.send(embed=embed)

@bot.command()
async def market(ctx):
    if not trade_offers:
        await ctx.send("⚠️ no active trade offers")
        return

    embed = discord.Embed(title="۶<:e01bl:1373340406472769586> ˖  __marketplace__", color=0x8FACCC)
    for user, offer in trade_offers[-10:]:  # show last 10
        embed.add_field(name=user, value=offer, inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    # Set status with no activity type
    await bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name="✿ — growing a garden"))

bot.run('YOUR_BOT_TOKEN')
