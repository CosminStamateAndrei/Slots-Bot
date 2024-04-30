import discord
from discord import Intents, Profile
from discord.ext import commands, tasks
import json
import timeit
import time
import os
import random
from PIL import Image, ImageFont, ImageDraw

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('It`s running')


def write_json(data):
    with open ('db.json', "w") as f:
        json.dump(data, f, indent=4)


@client.command()
async def register(ctx):
    hasAccount = False
    with open("db.json") as json_file:
        data = json.load(json_file)
        temp = data["users"]
        y = {"user_id": f"{ctx.author.id}", "name": f"{ctx.author.name}", "level": 1, "experience": 0, "multiplier": 1, "prevMess": 0,"prevAntispam": 0 ,"antispam": 0, "warns": 0, "moderator": "False", "coins": 0}
        for user in temp:
            if str(ctx.author.id) == user['user_id']:
                await ctx.send('```You already have an account```')
                hasAccount = True
        if hasAccount == False:
            temp.append(y)
            await ctx.send('```Account created succesfully```')
    write_json(data)

@client.command()
async def reg(ctx, member: discord.Member):
  hasAccount = False
  with open("db.json") as json_file:
      data = json.load(json_file)
      temp = data["users"]
      y = {"user_id": f"{member.id}", "name": f"{member.name}", "level": 1, "experience": 0, "multiplier": 1, "prevMess": 0,"prevAntispam": 0 ,"antispam": 0, "warns": 0, "moderator": "False", "coins": 0}
      for user in temp:
          if str(member.id) == user['user_id']:
              await ctx.send(f'```{member.name} already has an account```')
              hasAccount = True
      if hasAccount == False:
          temp.append(y)
          await ctx.send(f'```Account created succesfully for {member.name}```')
  write_json(data)


@client.command()
async def resetall(ctx):
    if ctx.author.id == 518331788880510979:
        with open("db.json") as json_file:
            data = json.load(json_file)
            temp = data["users"]
            for user in temp:
                user['level'] = 1
                user['experience'] = 0
                user['multiplier'] = 1
            await ctx.send(f'```The CEO {ctx.author.name} has reseted the database. Start from now on everybody has their stats set at 0.```')
            write_json(data)

@client.command()
async def reset(ctx, target: discord.Member):
    with open("db.json") as json_file:
        data = json.load(json_file)
        temp = data['users']
        isModerator = False
        for user in temp:
            if str(ctx.author.id) == user['user_id']:
                if user['moderator'] == "True":
                    isModerator = True
        for user in temp:
            if user['user_id'] == str(target.id):
                if user['moderator'] != "True" or ctx.author.id == 518331788880510979:
                    if isModerator:
                        user['level'] = 1
                        user['experience'] = 0
                        user['multiplier'] = 1
                        user['antispam'] = 0
                        user['warns'] = 0
                        await ctx.send(f'```User has been reseted. Now {target.name} stats are at 0.```')
                else:
                    await ctx.send('```You cannot reset a moderator```')
            write_json(data)

@client.command(aliases = ['rw'])
async def resetwarns(ctx, target: discord.Member):
    with open("db.json") as json_file:
      data = json.load(json_file)
      temp = data['users']
      for user in temp:
        if str(ctx.author.id) == user['user_id']:
          if user['moderator'] == "True":
            pass
          else:
            return
      for user in temp:
        if str(target.id) == user['user_id']:
          if user['moderator'] == "False":
            user['warns'] = 0
            await ctx.channel.send(f'```Wars reseted. {target.name}\'s warns are at 0.```')
          else:
            await ctx.channel.send(f'```{target.name} is also a moderator. You can not reset his warns.```')
    write_json(data)

@client.command(aliases = ['info'])
async def profile(ctx):
    with open("db.json") as json_file:
        data = json.load(json_file)
        temp = data['users']
        for user in temp:
            if str(ctx.author.id) == user['user_id']:
                embed = discord.Embed(
                    title='Stats',
                    colour=discord.Colour.red()
                )
                moderatorQuote = ''
                if user['moderator'] == "True":
                    moderatorQuote = 'moderator'
                else:
                    moderatorQuote = 'normal user'
                level = str(user['level'])
                experience = str(user['experience'])
                warns = str(user['warns'])
                coins = str(user['coins'])
                experienceTillLevel = str((5 * user['multiplier'])-user['experience'])
                embed.set_footer(text=f'This user is a {moderatorQuote}')
                embed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/748943736293163038/781270221637288006/1606073462735.png')
                embed.set_author(name=ctx.author.name,
                                icon_url=ctx.author.avatar_url)
                embed.add_field(name='Level', value=f'This person level is {level}',
                                inline=False)
                embed.add_field(name='Experience', value=f'This person has {experience} points of experience',
                                inline=False)
                embed.add_field(name='Warns', value=f'This person has {warns} warns',
                                inline=False)
                embed.add_field(name='EXP for next level', value=f'This person has {experienceTillLevel} points of experience till level up',
                                inline=False)
                embed.add_field(name='Coins', value=f'This person has {coins} PULA',
                                inline=False)
                await ctx.channel.purge(limit=1)
                await ctx.send(embed=embed)


@client.event
async def on_message(ctx):
    previouslyMessage = time.time()
    previouslyAntispam = 0.1
    if ctx.channel.id == 905261046749597706:
        await client.process_commands(ctx)
        return
    if ctx.author.bot == False:
        founduser = False
        with open("db.json") as json_file:
            data = json.load(json_file)
            temp = data["users"]
            y = {"user_id": f"{ctx.author.id}", "name": f"{ctx.author.name}", "level": 1, "experience": 0, "multiplier": 1, "prevMess": 0,"prevAntispam": 0 ,"antispam": 0, "warns": 0, "moderator": "False", "coins": 0}
            for user in temp:
                if str(ctx.author.id) == user['user_id']:
                    founduser = True
            if founduser == False:
                temp.append(y)
        write_json(data)
        with open("db.json") as json_file:
            data = json.load(json_file)
            temp = data["users"]
            for user in temp:
                if str(ctx.author.id) == user['user_id']: #found them
                    antispamVar = int(user['antispam'])
                    if previouslyMessage-user['prevMess'] < 2.6:
                        previouslyAntispam = time.time()
                        if antispamVar >= 2:
                            await ctx.channel.purge(limit=4)
                            await ctx.channel.send("```Spamming will get you no-where. No points of XP have been added. More spam will result you in getting a warn.```", delete_after=7)
                            if previouslyAntispam - user['prevAntispam'] < 3:
                                user['warns'] += 1
                                await ctx.channel.send(f'{ctx.author.mention} you have been warned by the anti-spamming system. You have currently ' + str(user['warns']) + ' warns. Watch out!', delete_after=7)
                            else:
                                user['antispam'] = 0
                                user['prevAntispam'] = previouslyAntispam

                        else:
                            user['antispam'] += 1
                    else:
                        user['prevMess'] = previouslyMessage
                        user['experience'] = user['experience'] + 1
                    if user['experience'] >= 5 * user['multiplier']:
                        user['multiplier'] += 0.8
                        user['experience'] = 0
                        user['level'] += 1
                        level = str(user['level'])
                        await ctx.channel.send(f'```You leveled up! Now your level is {level}```')
            write_json(data)
        await client.process_commands(ctx)


placesSlot = [
    [(349,183), (349,410), (349,637)],
    [(596,183), (596,410), (596,637)],
    [(844,183), (844,410), (844,637)],
    [(1095,183), (1095,410), (1095,637)],
    [(1344,183), (1344,410), (1344,637)],
]


@client.command()
async def spin(ctx, coinsToSpend):
    if coinsToSpend == None:
        return
    try:
        coinsToSpend = int(coinsToSpend)
    except Exception:
        return
    mainframe = Image.open("mainframe.png")
    cireasa = Image.open("Cirese.png")
    pruna = Image.open("Pruna.png")
    struguri = Image.open("Grapefruit.png")
    melon = Image.open("Melon.png")
    portocale = Image.open("portocale.png")
    septaru = Image.open("septaru.png")
    steluta = Image.open("Stelutza.png")
    lamaie = Image.open("Lamaie.png")

    cireasa = cireasa.resize((225, 227))
    pruna = pruna.resize((225, 227))
    struguri = struguri.resize((225, 227))
    melon = melon.resize((225, 227))
    portocale = portocale.resize((225, 227))
    septaru = septaru.resize((225, 227))
    steluta = steluta.resize((225, 227))
    lamaie = lamaie.resize((225, 227))

    results = [
        ["None", "None", "None"],
        ["None", "None", "None"],
        ["None", "None", "None"],
        ["None", "None", "None"],
        ["None", "None", "None"]
    ]

    font = ImageFont.truetype("arial.ttf", 48)
    draw = ImageDraw.Draw(mainframe)
    text = "1250"
    bet = str(coinsToSpend)
    win = 0

    items = [cireasa, pruna, struguri, melon, portocale, septaru, steluta, lamaie]

    for i in range(5):
        for j in range (3):
            num = random.randint(0, 7)
            mainframe.paste(items[num], placesSlot[i][j])
            if num == 0:
                results[i][j] = "cireasa"
            elif num == 1:
                results[i][j] = "pruna"
            elif num == 2:
                results[i][j] = "struguri"
            elif num == 3:
                results[i][j] = "melon"
            elif num == 4:
                results[i][j] = "portocale"
            elif num == 5:
                results[i][j] = "septaru"
            elif num == 6:
                results[i][j] = "steluta"
            elif num == 7:
                results[i][j] = "lamaie"

    for x in range(4):
        for y in range(3):
            if x==4:
                if results[x][y] == results[x-1][y]:
                    if results[x][y] == "cireasa":
                        if results[x][y] == results[x-2][y]:
                            await ctx.channel.send("Linie de 3 cirese")
                            win = coinsToSpend * 4
                        else:
                            await ctx.channel.send("Linie de 2 cirese")
                            win = coinsToSpend * 3
                    else:
                        if results[x][y] == results[x-2][y]:
                            if results[x][y] == "septaru":
                                await ctx.channel.send(f'Linie de 3 septari')
                                win = coinsToSpend*20
                            elif results[x][y] == "pruna":
                                await ctx.channel.send(f'Linie de 3 prune')
                                win = coinsToSpend*20
                            elif results[x][y] == "struguri":
                                await ctx.channel.send(f'Linie de 3 struguri')
                                win = coinsToSpend*20
                            elif results[x][y] == "melon":
                                await ctx.channel.send(f'Linie de 3 pepeni')
                                win = coinsToSpend*20
                            elif results[x][y] == "portocale":
                                await ctx.channel.send(f'Linie de 3 portocale')
                                win = coinsToSpend*20
                            elif results[x][y] == "steluta":
                                await ctx.channel.send(f'Linie de 3 stele')
                                win = coinsToSpend*20
                            elif results[x][y] == "lamaie":
                                await ctx.channel.send(f'Linie de 3 lamai')
                                win = coinsToSpend*20
            elif x==3:
                pass
                # if results[x][y] == results[x+1][y]:
                #     if results[x][y] == "cireasa":
                #         if results[x][y] == results[x-1][y]:
                #             await ctx.channel.send("Linie de 3 cirese")
                #             win = coinsToSpend*4
            else:
                if results[x][y] == results[x+1][y]:
                    if results[x][y] == "cireasa":
                        if results[x][y] == results[x+2][y]:
                            await ctx.channel.send("Linie de 3 cirese")
                            win = coinsToSpend*4
                        else:
                            await ctx.channel.send("Linie de 2 cirese")
                            win = coinsToSpend*3
                    else:
                        if results[x][y] == results[x+2][y]:
                            if results[0][y] == results[1][y] and results[0][y] == results[2][y] and results[0][y] == results[3][y] and results[0][y] == results[4][y]:
                                await ctx.channel.send(f'Linie de 5 {results[x][y]}') 
                                win = coinsToSpend*20
                            else:
                                if results[x][y] == "septaru":
                                    await ctx.channel.send(f'Linie de 3 septari')
                                    win = coinsToSpend*20
                                elif results[x][y] == "pruna":
                                    await ctx.channel.send(f'Linie de 3 prune')
                                    win = coinsToSpend*20
                                elif results[x][y] == "struguri":
                                    await ctx.channel.send(f'Linie de 3 struguri')
                                    win = coinsToSpend*20
                                elif results[x][y] == "melon":
                                    await ctx.channel.send(f'Linie de 3 pepeni')
                                    win = coinsToSpend*20
                                elif results[x][y] == "portocale":
                                    await ctx.channel.send(f'Linie de 3 portocale')
                                    win = coinsToSpend*20
                                elif results[x][y] == "steluta":
                                    await ctx.channel.send(f'Linie de 3 stele')
                                    win = coinsToSpend*20
                                elif results[x][y] == "lamaie":
                                    await ctx.channel.send(f'Linie de 3 lamai')
                                    win = coinsToSpend*20
    draw.text((425,876), text, (255,188,0), font=font)
    draw.text((961,876), bet, (255,188,0), font=font)
    draw.text((1437,876), str(win), (255,188,0), font=font)
    mainframe.save("result.png")

    await ctx.send(file = discord.File("result.png"))

    os.remove("result.png")


client.run('')