import discord
import database
import json

with open("pokemon.json", "r") as f:
    pokedex = json.load(f)

async def add_pokemon(user:discord.User, pokemon):
    db = await database.get(user)
    if not db["slot1"]:
        await database.modify(user, slot1=pokemon)
    elif not db["slot2"]:
        await database.modify(user, slot2=pokemon)
    elif not db["slot3"]:
        await database.modify(user, slot3=pokemon)
    elif not db["slot4"]:
        await database.modify(user, slot4=pokemon)
    elif not db["slot5"]:
        await database.modify(user, slot5=pokemon)
    elif not db["slot6"]:
        await database.modify(user.slot6=pokemon)
    else:
        for i in range(1,100):
            if len(db["boxes"][i]) < 30:
                new_boxes = db["boxes"].append(pokemon)
                await database.modify(user, boxes=new_boxes)
                break

async def sell_pokemon(ctx, user:discord.User, box, position):
    db = await database.get(user)
    boxpositions = {"a": -1, "b": 5, "c": 11, "d": 17, "e": 23}
    boxes = db["boxes"]
    if len(db["boxes"]) < box:
        await ctx.reply(f"You do not own a box {box}!")
    elif boxes[box][boxposition[position[0]]+position[1]]:
        pokemon = boxes[box][boxposition[position[0]]+position[1]]
        value = pokedex[pokemon["pokemon"]]
        class View(discord.ui.View):
            @discord.ui.button(label="Yes", style=discord.ui.ButtonStyle.success)
            async def yes(self, interaction):
              boxes[box].pop([boxposition[position[0]]+position[1]])
              new_boxes = boxes
              await database.modify(boxes=new_boxes)
              new_balance = db["balance"] += value
              await database.modify(balance=new_balance)
              interaction.response.send_message(f"Ok! Your pokemon has been sold and {value} PokeCoins have been added to your balance!")
            @discord.ui.button(label="No", style=discord.ui.ButtonStyle.danger)
            async def no(self, interaction):
                interaction.response.send_message("Oh ok. You can run this command again in the future to sell pokemon!")
        await ctx.reply(f"Are you sure you want to sell your Level {pokemon["level"]} {pokemon["pokemon"]} for {value} PokeCoins?")
    else:
        await ctx.reply("Hmmm. Seems like you do not have a pokemon in that position. Try checking the position of the pokemon you want to sell!")
        