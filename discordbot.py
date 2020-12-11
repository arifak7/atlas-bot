import discord

intents = discord.Intents.all()
client = discord.Client(fetch_offilne_members=True, intents=intents,activity=discord.Game(name="Your Dad 🍆"))
queue =list()
temp = list()
waiting_room=781440904019050499
among_us_1=781440904019050498
among_us_2=783492184040669204
role_message=785479442788778014
member_role=785480963009806367
auto_deafen=False #default
on_going=False
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    try:
        if (payload.message_id == role_message):
            if (payload.emoji.name == "❌"):
                await payload.member.remove_roles(payload.member.guild.get_role(member_role))
            if (payload.emoji.name == "✅"):
                await payload.member.add_roles(payload.member.guild.get_role(member_role))
    except Exception as e:
        await message.channel.send(e)


#queueing system

@client.event
async def on_voice_state_update(member, before, after):
    global on_going
    if ((after.channel) and after.channel.id == waiting_room):
        queue.append(member)

    if ((before.channel) and before.channel.id == waiting_room):
        if((after.channel) and (after.channel.id!=among_us_1)):
            queue.remove(member)
        if(not(after.channel)):
            queue.remove(member)


    # i have no clue why this works, but i use xnor to determine consistency between deaf and mute
    # then run a check with before to make sure the current action doesnt trigger future event
    # ending in endless loop cuz fuck that
    # and member.guild_permissions.administrator and auto_deafen
    if (after and (after.channel)and member.guild_permissions.administrator and auto_deafen):
        if(not(after.self_deaf ^ after.self_mute)):
            if(not on_going):
                on_going=True
                users = member.voice.channel.members
                for user in users:
                    await user.edit(deafen=after.self_deaf, mute=after.self_mute)
                on_going=False

    #check if channel 10 or more
    if (len(member.guild.get_channel(among_us_1).members) ==9):
        if ((((before.channel) and before.channel.id == among_us_1) and queue) and ((after.channel) and after.channel.id==waiting_room)):
            # to avoid error, checking if the user is in the channel without removed in queue
            for user in queue:
                if ((user.voice) and user.voice.channel.id == waiting_room):
                    try:
                        if (len(user.guild.get_channel(among_us_1).members) < 10):
                            queue.pop(0)
                            await user.move_to(user.guild.get_channel(among_us_1))
                    except Exception as e:
                        queue.insert(0, user)
                        await message.channel.send(e)
                else:
                    queue.pop(0)
@client.event
async def on_member_join(member):
    try:
        await member.add_roles(member.guild.get_role(781443027604471859))
    except Exception as e:
        await message.channel.send(e)


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if (message.content.startswith("!q")):
        tmp="Queue:\n"
        x=1
        for user in queue:
            tmp+= str(x)+"."+user.name+"\n"
            x+=1
        await message.channel.send(tmp)

    if (message.content.startswith("!get rolled Loue")):
        await message.channel.send("https://cdn.discordapp.com/emojis/786825616531914794.gif?v=1")

    if (message.content.startswith("!ad")):
        if (message.author.guild_permissions.administrator):
            global auto_deafen
            auto_deafen = not auto_deafen
            tmp = "AutoDeafen is"
            tmp += " enabled" if auto_deafen else " disabled"
            await message.channel.send(tmp)

    if (message.content.startswith("!d")):
        try:
            member = message.author
            if (member.guild_permissions.administrator):
                users = message.mentions if message.mentions else message.author.voice.channel.members
                for user in users:
                    await user.edit(deafen=not (user.voice.deaf), mute=not (user.voice.mute))
        except Exception as e:
                await message.channel.send(e)

client.run('Nzg0MjA5Mjg3NzcyODk3MzMw.X8l90A.ynoCu0yRkcgqE_pOKMfbHbOVt-c')
