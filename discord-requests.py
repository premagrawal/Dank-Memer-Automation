import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
login_id = ""
password = ""
channel_id = ""
##################################################################################################################
def tokenGen():
    headers = {
        'content-type': 'application/json',
    }
    data = '{"login":"'+login_id+'","password":"'+password+'"}'
    response = requests.post('https://discord.com/api/v9/auth/login',headers=headers,data=data)
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        driver = webdriver.Chrome()
        driver.get('https://discord.com/login')
        driver.maximize_window()
        driver.find_element_by_name('email').send_keys(login_id)
        driver.find_element_by_name('password').send_keys(password)
        driver.find_element_by_name('password').send_keys(Keys.ENTER)
        time.sleep(10)
        driver.quit()
        time.sleep(10)
        response = requests.post('https://discord.com/api/v9/auth/login',headers=headers,data=data)
    token = str(json.loads(response.text)['token'])
    return token
##################################################################################################################
def sendMessage(token,message):
    url       = "https://discord.com/api/v9/channels/"+channel_id+"/messages"
    payload   = {"content":str(message)}
    header    = {'authorization': token}
    response  = json.loads(requests.post(url,data=payload,headers=header).text)
    message   = response['content']
    timestamp = ((response['timestamp'].split('T'))[1].split('.')[0])
    response  = str('Message {} sent at : {}'.format(message,timestamp))
    return response
##################################################################################################################    
def getMessage(token):
    url       = "https://discord.com/api/v9/channels/"+channel_id+"/messages"
    header    = {'authorization': token}
    response  = json.loads(requests.get(url,headers=header).text)
    return response[0]['content']
##################################################################################################################        
def buyItem(token,item):
    response  = sendMessage(token=token,message="pls with max")
    item      = "pls buy " + str(item)
    time.sleep(1)
    response  = sendMessage(token=token,message=item)
    message   = str(getMessage(token=token))
    time.sleep(1)
    response  = sendMessage(token=token,message="pls dep max")
    return message
##################################################################################################################        
commands  = ['pls dig','pls beg','pls hunt','pls fish']
notSell   = ['worms','junk','seaweed','duck','boar','skunk','bread','ant','alcohol','fish','deer','rabbit','rarefish','exoticfish','sand']
token     = tokenGen()
notRifle  = "You don't have a hunting rifle, you need to go buy one. You're not good enough to shoot animals with your bare hands."
notPole   = "You don't have a fishing pole, you need to go buy one. You're not good enough to catch them with your hands."
notShovel = "You don't have a shovel, you need to go buy one. I'd hate to let you dig with your bare hands."
nothingOne= "LMAO you found nothing. NICE!"
nothingTwo= "You went hunting in the woods and brought back NOTHING! 😆"
while True:
    #response = sendMessage(token=token,message="pls with max")
    #print(getMessage(token=token))
    #response = sendMessage(token=token,message="pls buy horseshoe")
    #print(getMessage(token=token))
    #response = sendMessage(token=token,message="pls dep max")
    #print(getMessage(token=token))
    #response = sendMessage(token=token,message="pls use horseshoe")
    #print(getMessage(token=token))
    for count in range(1,20):
        #print(count)
        for index in range(0,len(commands)):
            response = sendMessage(token=token,message=commands[index])
            time.sleep(2)
            message = str(getMessage(token=token))
            shoeActive = str((message.split(' <:')[-1]).split(':')[0])
            response = sendMessage(token=token,message="pls dep max")
            time.sleep(2)
            if message == notRifle :
                message = buyItem(token=token,item="rifle")
                print(message)
            elif message == notPole :
                message = buyItem(token=token,item="pole")
                print(message)
            elif message == notShovel :
                message = buyItem(token=token,item="shovel")
                print(message)
            elif message == nothingOne or message == nothingTwo:
                print(' Found Nothing ')
            elif shoeActive != "horseshoe":
                response = sendMessage(token=token,message="pls use horseshoe")
                time.sleep(1)
                message  = getMessage(token=token)
                if message == "You don't own this item??":
                    print('Buying Horseshoe')
                    response = buyItem(token=token,item="horseshoe")
                    time.sleep(1)
                    print(response)
                    response = sendMessage(token=token,message="pls use horseshoe")
                    time.sleep(1)
                    message  = getMessage(token=token)
                    print(message) 
            else :
                print(message)
        time.sleep(30)
