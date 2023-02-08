from random import randint, random
import discord
import datetime  
import bs4 
import urllib
import random
import time 



channel = 0

client = discord.Client(intents=intents)

def timeCheck():
    global sch 
    global channel

    
    timeNow = datetime.datetime.now()
    timeFormatted = timeNow.strftime("%I%p")
    print(timeFormatted + ":" + str(int(timeNow.strftime("%I"))<10))

    if int(timeNow.strftime("%I")) < 10:
        getNews(channel)

async def timedSend(channel,fake):
    while channel != 00000000:
        await getNews(channel,fake)
        time.sleep(5)



async def getNews(channel,fake):
    doneFake=False
    titles = []
    contents = []

    url =  urllib.request.urlopen("https://www.pcgamer.com/news/")
    soup = bs4.BeautifulSoup(url.read(), "html.parser")
    newsHTML = soup.find_all("article",{"class":"search-result search-result-news has-rating"})
    newsTitles = soup.find_all("h3",{"class":"article-name"})
    newsContent = soup.find_all("p",{"class":"synopsis"})

    for title in newsTitles:
        titles.append(title.get_text())
    for content in newsContent:
        contents.append(content.get_text().strip("news").strip("News"))

    await client.get_channel(channel).send("**5 most Recent News Articles from PCGamer.com** \n ---------------------------------------------")
    for x in range(5):
        newChannel = client.get_channel(channel)
        if fake and random.randint(0,1)==1 and not doneFake:
            choice = randint(0,len(fakeTitles)-1)
            await newChannel.send(f"***{fakeTitles[choice]}*** \n\n{fakeContent[choice]} \n____________________")
            fakeTitles.pop(choice)
            fakeContent.pop(choice)
            doneFake = True
        else:    
            try:
                await newChannel.send(f"***{titles[x]}*** \n {contents[x]} ____________________")
            except:
                print("Failed to send news")



##################


@client.event
async def on_ready():
    global sched

    print(f'Logged in as {client.user}')
    #sched.add_job(timeCheck,'interval', minutes=0.05)









@client.event
async def on_message(message):
    global channel



    with open("mssglog.txt","a+") as file:
        print(channel==message.channel.id)
        print(f"{message.author}:{message.content}")
        if channel==message.channel.id:
            file.write(f"{message.author}:{message.content}\n")


    if message.author == client.user:
        return
    


    if message.content.startswith('.CHANNEL=') and (message.author.id == 511729306901413896 or message.author.id == 484534047398428692) :
        channel = int(message.content[9::])
        await message.channel.send(f"Set CHANNEL to {channel}")

    if message.content.startswith(".NEWS" ) and (message.author.id == 511729306901413896 or message.author.id == 484534047398428692): #This is purely for testing purposes - should be commented out when actually using bot
        #await getNews(channel,False)
        await timedSend(channel,False)
        #thread1 = threading.Thread(target=timedSend,daemon=False,args=[channel,False]) 

    

client.run('MTAyNjY3Njg3MTEwNDAzNjk0NQ.GSsH_6.E_-VvgTyZoQ7IhF9XOUPHT8VbKWylgi8Q-LJmc')
