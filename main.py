# Importing libraries

from urllib.request import Request, urlopen
import json
import datetime
import json
import discord
from discord import SyncWebhook




# The title of the embed message
# You can use 2 variables: 
# dayEnglish is Monday
# dayFinnish is Maanantain
title = "dayEnglish food"

# Subtitles
lunchTitle = "Lunch"
vegLunchTitle = "Vegetarian lunch"

# See the github page for more info
customerID = 12345

# See the github page for more info
kitchenID = 1

# I haven't played around with this
language = "fi" 

# You can have multiple webhooks the bot sends the embed to
webhooks = ["WEBHOOK URL HERE"]

# These items in the menu will be not be sent with the embed
ignoreItems = ["Aterialisät", "Tarkista aina sisältötiedot linjastosta!", "tai kysy henkilökunnalta"]





try:
    # Gets the names of the days.
    now = datetime.datetime.now()
    dayEnglish = str(now.strftime("%A"))
    if dayEnglish == "Saturday" or dayEnglish == "Sunday":
        exit()
    if dayEnglish == "Monday":
        dayFinnish = "Maanantain"
    elif dayEnglish == "Tuesday":
        dayFinnish = "Tiistain"
    elif dayEnglish == "Wednesday":
        dayFinnish = "Keskiviikon"
    elif dayEnglish == "Thursday":
        dayFinnish = "Torstain"
    elif dayEnglish == "Friday":
        dayFinnish = "Perjantain"
    
    # Date to specify the time frame in the request
    urlDate = str(now.strftime("%Y%m%d"))

    # Requests the JSON page
    req = Request(
        url="https://fi.jamix.cloud/apps/menuservice/rest/haku/menu/" + str(customerID) + "/" + str(kitchenID) + "?lang=" + str(language) + "&date=" + urlDate + "&date2=" + urlDate, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    # Getting the JSON and the correct path for the menu items
    webpage = urlopen(req)
    pageJson = json.loads(webpage.read())
    path = pageJson[0]["menuTypes"][0]["menus"][0]["days"][0]["mealoptions"]

    # Adding menu items to lunch menus 

    lunchMenu = []
    vegLunchMenu = []
    loopCounting = 0
    for mealOption in path:
        loopCounting = loopCounting + 1
        for mealOptionSub in mealOption["menuItems"]:
            if mealOptionSub["name"] in ignoreItems:
                continue
            if loopCounting == 1:
                lunchMenu.append(mealOptionSub["name"])
            else:
                vegLunchMenu.append(mealOptionSub["name"])


    # Removing duplicates in the vegetarian menu
    # V This can be removed if you want duplicate items V

    for item in lunchMenu:
        if item in vegLunchMenu:
            vegLunchMenu.remove(item)
    
    # ^ This can be removed if you want duplicate items ^


    # This part sends the embeds to the webhooks

    for webhook in webhooks:

        # Titles
        embed=discord.Embed(title=" ")
        embed.set_author(name=title.replace("dayEnglish",dayEnglish).replace("dayFinnish",dayFinnish))

        # Add commas and spaces
        lunchMenu2 = ", ".join(lunchMenu)
        vegLunchMenu2 = ", ".join(vegLunchMenu)

        # 
        embed.add_field(name=lunchTitle, value=lunchMenu2, inline=False)
        if len(vegLunchMenu) != 0:
            embed.add_field(name=vegLunchTitle, value=vegLunchMenu2, inline=False)

        # Send embed to webhook
        webhook = SyncWebhook.from_url(webhook)
        webhook.send(embed=embed)

# Error handling
except Exception as e:
    print("Something went wrong: " + str(e))
