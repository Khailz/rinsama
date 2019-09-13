#!/usr/bin/python
# --------------------------------------------------------------------------------
# Rin~Sama Alpha v0.7
# ---------------------
# Functions:
# #
# connect to theunlighted.com teamspeak ?
# Connect to theunlighted.io django api or DB ?
# Authenticate user account on website with teamspeak ?
# AniList Search Support ?
# MAL account connection
# Point system both website and Rin~Sama ?
# Create requested channels "After donation"
# Purchase Bot with Paypal ?
# IRC type mini games such as history questions, roulette, dice, etc ?
# Twitch authentication
# Reward with server groups ?
# News feature
# Leaderboards ? sort fo
# AIML supprt if I can do it :D
# ---------------------------------------------------------------------------------

# Installed packages in library
import sys, os, hashlib, praw, re
import random, datetime
import threading
import json
import logging
import uuid
import pickle
import socket
import time
import ts3
import requests, textwrap



# Other Packages


from sayings import reply, sayings
from threading import Thread
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

default_settings = {"notify": {}}

__all__ = ["hello_bot"]

class Functions(object):
    def __init__(self):
        pass

    @classmethod
    def refresh_user_all(self):

        try:
            print("Searching for new users")

            url = "{}".format(settings.api_url)
            headers = {'Content-type': 'application/json'}

            r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))

            with open(BASE_DIR + '\current_users.txt', 'w+') as outfile:
                json.dump(r.json(), outfile)
                print("Saved Current UNLIGHTED USERS ro current_users.txt")
            return r.json()
        except requests.exceptions.ConnectionError as e:
            print(e)
            pass

    def check_user(chkkey):
        print("Checking for user")
        with open(BASE_DIR + '/current_users.txt') as json_data:
            usr_json = Functions.refresh_user_all()
        for x in usr_json:
            try:
                email = x['email']
                points = x['points']
                ts3id = x['settings']['ts3']['ts3_identity']
                username = x['username']
                userid = x['url']
                userid = re.sub('[^0-9]','', userid)
                linkkey = x['settings']['ts3']['link_key']
            except KeyError as e:
                continue
            if ts3id == chkkey:
                print("User found")
                return username, userid, email, ts3id, points, linkkey

        Functions.refresh_user_all()

    def ts3connect(ts3iuid, usersiteid):

        try:
            found = False

            url = "{}".format(settings.api_url)
            headers = {'Content-type': 'application/json'}
            r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
            for user in r.json():
                try:
                    if user['settings']['ts3']['ts3_identity'] == ts3iuid:
                        found = True
                        print("Found user on THEUNLIGHTED: {}".format(user['username']))
                        break
                except KeyError as e:
                    #print('I got a KeyError - reason "%s"' % str("No Ts3 found for user {}".format(user['username'])))
                    continue

            if found is False:
                headers = {'Content-type': 'application/json'}
                salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
                activation_key = hashlib.sha1(salt.encode('utf-8') + str(ts3iuid).encode('utf-8')).hexdigest()
                a = datetime.datetime.today()
                b = a + datetime.timedelta(0, 300)  # days, seconds, then other fields.
                url = "{}".format(settings.api_url) + '{}'.format(usersiteid)
                print(url + ' ' + activation_key)
                payload = {"settings": {"ts3_identity": ts3iuid, "activation_key": activation_key, "key_expires": str(b).replace(" ", "T")}}
                r = requests.post(url, headers=headers, data=json.dumps(payload), auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                print(r.text)

                return activation_key

            if found:
                url = "{}".format(settings.api_url)
                headers = {'Content-type': 'application/json'}
                r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                for user in r.json():
                    try:
                        if user['settings']['ts3']['ts3_identity'] == ts3iuid:
                            return user['settings']['ts3']["activation_key"]
                            break
                    except KeyError as e:
                        print('I got a KeyError - reason "%s"' % str(e))
                        continue
        except TypeError as e:
            print(e + "Hi")

    def chckuseropts(chkkey):
        try:

            url = "{}".format(settings.api_url)
            headers = {'Content-type': 'application/json'}

            r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
            for key in r.json():

                ts3id = key['ts3_identity']
                settings = key['settings']['opts']
                print(settings)
                if ts3id == chkkey:
                    return settings

        except TypeError as e:
            print(e)

    def useroptsadd(ts3iuid):

        try:
            username, userid, email, ts3id, points, linkkey = Functions.check_user(chkkey=ts3iuid)
            print(userid, default_settings)
            url = "{}".format(settings.api_url) + '{}'.format(userid)
            r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
            settings = r1.json()["settings"]
            settings["opts"] = {}
            url = "{}".format(settings.api_url) + '{}'.format(userid)
            payload = {"settings": json.dumps(settings)}
            r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
            print(r.status_code)

            return r.status_code
        except TypeError as e:
            print(e)

    def masspoke(msg):

        for client in ts3conn.clientlist():
            if client['client_type'] == '1' or client['client_database_id'] == '1':
                continue
            else:
                ts3conn.clientpoke(msg="""{} ~{}""".format(msg, event.parsed[0]['invokername']), clid=client['clid'])

    def optin(key):
        cliuid = event.parsed[0]['invokeruid']
        username, userid, email, ts3id, points, linkkey = Functions.check_user(chkkey=cliuid)
        try:
            url = "{}".format(settings.api_url) + '{}'.format(userid)
            r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.user)))
            oldsettings = r1.json()["settings"]
            opts = oldsettings["opts"]
        except KeyError:
            ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['invokerid'],
                                    msg="No Opt config found. Creating one...")
            Functions.useroptsadd(ts3iuid=ts3id)
            ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['invokerid'], msg="Done.")
        try:
            url = "{}".format(settings.api_url) + '{}'.format(userid)
            r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.user)))
            oldsettings = r1.json()["settings"]
            opts = oldsettings["opts"]
            opts['{}'.format(key)] = True
            url = "{}".format(settings.api_url) + '{}'.format(userid)
            payload = {"settings": json.dumps(oldsettings)}
            r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.user)))
            print(r.status_code)
            ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['invokerid'],
                                    msg="Optted in for Anime Notifications!")
            return r.status_code
        except TypeError as e:
            print(e)

    def movetochan(ts3conn):
        ts3conn.clientmove(cid=Functions.getclinfomsg(sender, event)[0], clid=me)

    def movebackchan(ts3conn):
        ts3conn.clientmove(cid=209, clid=me)

    def gettoken():
        url = 'https://anilist.co/api/auth/access_token'

        data = {'grant_type': "client_credentials",
                'client_id': '{}'.format(settings.ani_cli),
                'client_secret': '{}'.format(settings.ani_cli_secret)
                }
        r = requests.post(url, params=data)

        accessinfo = json.loads(r.text)
        token = accessinfo['access_token']

        # print("Access Granted, access token is " + token)

        return accessinfo['access_token']

class Features(object):
    def getusersettings(chkkey):

        try:

            url = "{}".format(settings.api_url)
            headers = {'Content-type': 'application/json'}

            r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.user)))
            for key in r.json():

                ts3id = key['ts3_identity']
                settings = key['settings']

                if ts3id == chkkey:
                    return settings
        except TypeError as e:
            print(e)

    def gettoken():
        url = 'https://anilist.co/api/auth/access_token'
        data = {'grant_type': "client_credentials",
                'client_id': '{}'.format(settings.ani_cli),
                'client_secret': '{}'.format(settings.ani_cli_secret)
                }
        r = requests.post(url, params=data)
        accessinfo = json.loads(r.text)
        token = accessinfo['access_token']
        return accessinfo['access_token']

    def checkrelease(search):
        url = 'https://anilist.co/api/anime/{}'.format(search)
        params = {'access_token': '{}'.format(Features.gettoken())}
        r = requests.get(url, params=params)
        return r.json()['title_english'], r.json()['airing']['countdown']

    def checkusers():
        print("Aninotify scan started")
        try:

            url = "{}".format(settings.api_url)
            headers = {'Content-type': 'application/json'}
            opted = 0
            unopted = 0
            r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.user)))
            print(r.json())
            for key in r.json():
                print(key)
                try:
                    settings = key['settings']['opts']
                    print(settings['Aninotify'])
                    if settings['Aninotify'] == True:
                        try:
                            Features.check_anime_times(ts3uid=key["ts3_identity"])
                            opted += 1
                        except ts3.query.TS3QueryError as err:
                            print(key['username'] + " could not be notified.")
                            if err.resp.error["id"] != "1281":
                                continue

                except KeyError:
                    unopted += 1
                    continue
            try:
                ts3conn.clientupdate(CLIENT_NICKNAME='Rin~Sama 0.9.18')

            except AttributeError:
                print('ERRRRROORRR')
            print("Aninotify run results: {} users notified | {} users not opted.".format(opted, unopted))
        except TypeError as e:
            print(e)

    def check_anime_times(ts3uid):
        clid = int(1)
        try:
            for client in ts3conn.clientgetids(cluid="{}".format(ts3uid)):
                clid = client["clid"]
        except AttributeError:
            print('Error checking for Anime')
        listtext = ""
        clisettings = Features.getusersettings(chkkey=ts3uid)
        for anime, title in clisettings['notify'].items():
            try:
                title, a = Features.checkrelease(search=anime)
            except TypeError:
                continue
            m, s = divmod(a, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            c = '[color=green]{}[/color]'.format(title) + ': ' + '[color=blue]{}[/color]'.format(
                "{0} releases in {1} days {2} hours {3} minutes {4} seconds".format(title, d, h, m, s))
            listtext = listtext + c + '\n'

        print("Client id {} notified".format(clid))
        try:
            ts3conn.clientupdate(CLIENT_NICKNAME='New Notification')
            ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="\n[B][U]AniNotify[/U][/B]\n{}".format(listtext))
            ts3conn.clientupdate(CLIENT_NICKNAME='E.R.I.S')
            ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="_____________________________________")
        except AttributeError:
            print('Error connecting to TS3 Server')
class CommandDispatcher:
    dispatcher = {
        '!optin': '',
        '!findani': '',
        '!love': '',
        '!myprofile': ''

    }


def hello_bot(ts3conn, event, msg=None):
        if event.event == 'notifycliententerview':
            if event.parsed[0]["client_type"] == "1":
                pass
            else:
                try:
                    print("Sending message to user!")
                    userinfo = Functions.check_user(chkkey=event.parsed[0]['client_unique_identifier'])
                    print(userinfo)
                    username, userid, email, ts3id, points, linkkey = userinfo
                    if userinfo:
                        cliuid = event.parsed[0]['client_unique_identifier']
                        # Functions.addpoints(cliuid=cliuid, addpnt=1)
                        # Functions.levergroupassign(ts3conn, points)
                        if len(str(points)) < 4:
                            points = "{} [color=#333399]points![/color]  ".format(points)
                        else:
                            points = "{} [color=#333399]points![/color] ".format(points)
                        ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'],
                                                    msg=reply['welcomemsgreg'].format(username, points))
                except TypeError:
                    try:
                        # userinfo = Functions.check_user(chkkey=event.parsed[0]['clid'])
                        # username, userid, email, ts3id, points, linkkey = userinfo
                        print("User not fully registered for Teamspeak")
                        tsconnecto = Functions.ts3connect(ts3iuid=event.parsed[0]["client_unique_identifier"], usersiteid=2)
                        #print("OI {}".format(event.parsed[0]["client_unique_identifier"]))
                        ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'],
                                                msg=reply['welcomenonreg'].format(tsconnecto))
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "770":
                            print("Ignoring user in channel...")
                except KeyboardInterrupt:
                    print('No duh')


def rin():

    with ts3.query.TS3Connection(HOST, PORT) as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=SID)
        me = ts3conn.whoami()[0]['client_id']
        ts3conn.clientupdate(CLIENT_NICKNAME='E.R.I.S')
        # Move the bot to the channel
        ts3conn.clientmove(cid=209, clid=me)
        ts3conn.servernotifyregister(event="server")
        ts3conn.servernotifyregister(event="channel", id_=0)
        ts3conn.servernotifyregister(event="textchannel")
        ts3conn.servernotifyregister(event="textprivate")

        # Register notifs and handle in new thread
        # func = Functions()
        # func.refresh_user_all()
        # hello_bot(ts3conn)
        while True:

            ts3conn.send_keepalive()

            try:
                # This method blocks, but we must sent the keepalive message at
                # least once in 10 minutes. So we set the timeout parameter to
                # 9 minutes.
                event = ts3conn.wait_for_event(timeout=550)
            except ts3.query.TS3TimeoutError:
                pass
            else:
                event = ts3conn.wait_for_event()
                print(event[0])
                # Greet new clients.
                if event.event == 'notifycliententerview':
                    print("HI")
                    hello_bot(ts3conn, event=event)

                notifytextmessage = event.event == 'notifytextmessage'

                if notifytextmessage:
                    clid = event.parsed[0]['invokerid']
                    cliuid = event.parsed[0]['invokeruid']

                    msg = event.parsed[0]['msg']

                    if msg.startswith('!'):
                        if msg.startswith('!mp') or msg.startswith('!MP'):
                            msg = msg[3:]
                            Functions.masspoke(msg=msg)

if __name__ == "__main__":
    USER = "serveradmin"
    PASS = "{}".format(settings.password)
    HOST = "{}".format(settings.ts_url)
    PORT = 10011
    SID = 1
    # app.run(threaded=True, debug=True)
    # flaskThread = threading.Timer(app.run(threaded=True, debug=True), ())
    # flaskThread.start()
    rinThread = threading.Timer(rin(), ())
    rinThread.start()


