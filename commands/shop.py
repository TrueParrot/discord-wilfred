import discord
from discord.ext import commands
import utils.logging as log
import utils.colours as colour
import utils.values as value
import utils.database as sql
from utils.helpers import *


class Shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def shop(self, ctx):
        log.debug("%s issued server command %s" % (str(ctx.message.author), str(ctx.message.content)))
        args = ctx.message.content.split()
        if len(args) == 1:
            shop_string = """1) **Custom Tag** -  __$15.00__
A custom role for you, permanent, no hoist or color

2) **Custom Profile Colour** -  __$10.00__
Stand out with a custom profile border. (Once a colour is chosen you cannot change it again without purchasing another)

3) **1 Week Custom Role** - __$5.00__
Aqua Coloured role with a name of your choice

4) **1000 Exp** - __$2.50__
Help boost your level with this exp bonus

5) **1 Crate** - __$1.00__
Open the crate to see what's inside
            """
            shopEm = discord.Embed(description="List of Purchasable Items\n" +shop_string , color=colour.primary)
            shopEm.set_author(name="Shop")
            shopEm.add_field(name="How to use the shop", value="You can obtain balance through being the most active each week, once you have enough balance to purchase an item on the shop, type !shop buy <item> <quantity>", inline=False)
            await ctx.send(embed=shopEm)
        else:
            if args[1].upper() == "BUY":
                bal = fetch_balance(ctx.author)
                if len(args) > 3:
                    quantity = int(args[3])
                else:
                    quantity = 1
                if args[2] == "1":
                    if bal >= 15.00:
                        add_balance(ctx.author, -15.00)
                        await ctx.send("Purchase Successful, Please contact a member of staff to request your tag!")
                    else:
                        em = discord.Embed(title = "Purchase Failed", description = "Insufficient Funds", color = colour.reds)
                        await ctx.send(embed=em)

                elif args[2] == "2":
                    if bal >= 10.00:
                        add_balance(ctx.author, -10.00)
                        await ctx.send("Purchase Successful, Please contact a member of staff to request your profile colour!")
                    else:
                        em = discord.Embed(title = "Purchase Failed", description = "Insufficient Funds", color = colour.reds)
                        await ctx.send(embed=em)

                elif args[2] == "3":
                    if bal >= 5.00:
                        add_balance(ctx.author, -5.00)
                        em = discord.Embed(title = "Purchase Successful", description = "Please contact a member of staff to request your role!", color = colour.primary)
                        await ctx.send(embed=em)
                    else:
                        em = discord.Embed(title = "Purchase Failed", description = "Insufficient Funds", color = colour.reds)
                        await ctx.send(embed=em)

                elif args[2] == "4":
                    if bal >= 2.50*float(quantity):
                        add_balance(ctx.author, -2.50*float(quantity))
                        em = discord.Embed(title = "Purchase Successful", description = "You have been given **%s** exp!" % (str(1000*quantity)), color = colour.primary)
                        await ctx.send(embed=em)
                        add_exp(ctx.author.id, 1000*quantity)
                        await check_level_up(ctx.author.id, ctx.guild, ctx.channel)
                    else:
                        em = discord.Embed(title = "Purchase Failed", description = "Insufficient Funds", color = colour.reds)
                        await ctx.send(embed=em)

                elif args[2] == "5":
                    if bal >= 1.00*float(quantity):
                        crates_no = sql.db_query("ibm.db", "SELECT crates FROM Members WHERE UserID = %s" % (str(ctx.author.id)))[0][0]
                        if crates_no + quantity > 15:
                            em = discord.Embed(title = "Error", description = "You can not have more than 15 crates in your inventory", color = colour.reds)
                            await ctx.send(embed=em)
                        else:
                            add_balance(ctx.author, -1.00*float(quantity))
                            em = discord.Embed(title = "Purchase Successful", description = "You have been given **%s** crate(s)!" % (str(1*quantity)), color = colour.primary)
                            await ctx.send(embed=em)
                            crates_no = crates_no + 1*quantity
                            sql.execute_query("ibm.db", "UPDATE Members SET crates = %s WHERE UserID = %s" % (str(crates_no), str(ctx.author.id)))
                    else:
                        em = discord.Embed(title = "Purchase Failed", description = "Insufficient Funds", color = colour.reds)
                        await ctx.send(embed=em)

                else:
                    em = discord.Embed(title = "Invalid Item!", description = "Use `!shop` to view list of items", color = colour.reds)
                    await ctx.send(embed=em)



def setup(client):
    client.add_cog(Shop(client))
