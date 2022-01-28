import threading
import requests
import json
import random
import sys

scsResponse = "<Response [200]>"

if len(sys.argv) == 3:
    print("DISPORT")
    print("By: Localt")
    print("##############")

    url = "https://discord.com"
    email = sys.argv[1]
    password = sys.argv[2]

    session = requests.Session()
    session.get(url)
    cookies = session.cookies.get_dict()

    print("Sending login request..")
    loginResponse = requests.request(
    "POST", 
    url+"/api/v9/auth/login", 
    json = {
        "login": email,
        "password": password
    },
    headers = {
        'cookie': cookies["__dcfduid"],
        'Content-Type': "application/json"
    })
    
    loginSuccess = False

    if  str(loginResponse) == scsResponse:
        loginSuccess = True
    else:
        print("Couldn't log in.")

    ###################

    if loginSuccess:
        token = json.loads(loginResponse.text)["token"]
        auth_header = {
            'cookie': cookies["__dcfduid"],
            'authorization': token,
            'Content-Type': "application/json"
        }

        userResponse = requests.request("GET", url+"/api/v9/users/@me", headers = auth_header)
        username = json.loads(userResponse.text)["username"]
        userid =  json.loads(userResponse.text)["id"]
        
        print("Successfully logged in as " + username)

        def createNonce():
            nonce = ""
            for digit in range(1,16):
                nonce += str(random.randint(0,9))
            return nonce

        def sendMessage(ts_msg, channel):
            sendresponse = requests.request("POST", url+"/api/v9/channels/"+channel+"/messages", json = {
                "content": ts_msg,
                "nonce": str(createNonce()),
                "tts": False
            }, headers = auth_header)
            if str(sendresponse) != scsResponse:
                print("Failed sending message.")

        ###################
        
        channel = input("Enter channel ID: ")

        lst_msg = ""
        def display():
            while True:
                displayRes = requests.request("GET", url+"/api/v9/channels/"+channel+"/messages", headers = auth_header)
                olderMsgs = json.loads(displayRes.text)
                user_old = olderMsgs[0]["author"]["id"]

                if user_old != userid:
                    td_msg = "<" + olderMsgs[0]["author"]["username"] + "> " + olderMsgs[0]["content"]
                    global lst_msg
                    if lst_msg != td_msg:

                        lst_msg = td_msg
                        print(lst_msg)

        def dt_inp():
            while True:
                if lst_msg != "":
                    msg = input()
                    sendMessage(msg, channel)
                
        if __name__ == "__main__":
            t1 = threading.Thread(target = display)
            t2 = threading.Thread(target = dt_inp)
            t1.daemon = True
            t2.daemon = True
            t1.start()
            t2.start()
            while True:
                pass