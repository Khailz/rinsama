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
import sys, os, hashlib, praw
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

logging.basicConfig(filename='rinlog.log',level=logging.ERROR,
        format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

default_settings = {"notify": {}}

def main():
    class Functions:

        def getclinfomsg(sender, event):
            try:
                clid = event.parsed[0]['invokerid']
                info = ts3conn.clientinfo(clid=clid)
                for client in info:
                    cid = client['cid']
                    name= client['client_nickname']
                    cliuid = client['client_unique_identifier']
                    clid = clid
                    cldbid = client['client_database_id']
                    clitc = client['client_totalconnections']
                    clidit = client['client_idle_time']
                    cliadr = client['connection_client_ip']
                    return cid, name, cliuid, clid,\
                            cldbid, clitc, \
                            clidit, cliadr
            except TypeError:
                pass

        def getclinfoid(sender, event):
            try:
                clid = event.parsed[0]['clid']
                info = ts3conn.clientinfo(clid=clid)
                for client in info:
                    cid = client['cid']
                    name= client['client_nickname']
                    cliuid = client['client_unique_identifier']
                    clid = clid
                    cldbid = client['client_database_id']
                    clitc = client['client_totalconnections']
                    clidit = client['client_idle_time']
                    cliadr = client['connection_client_ip']
                    return cid, name, cliuid, clid,\
                            cldbid, clitc, \
                            clidit, cliadr
            except ts3.query.TS3QueryError:
                pass
            except ts3.response.TS3ParserError:
                pass

        def checkusers(chkkey):

            try:

                url = "{}".format(settings.api_url)
                headers = {'Content-type': 'application/json'}

                r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                for key in r.json():

                    email = key['email']
                    points = key['points']
                    ts3id = key['ts3_identity']
                    username = key['username']
                    userid = key['id']
                    linkkey = key['link_key']

                    if ts3id == chkkey or linkkey == chkkey:
                        return username, userid, email, ts3id, points, linkkey
            except TypeError as e:
                print(e)
                pass

            except ValueError as e:
                pass

            except requests.exceptions.ConnectionError as e:
                print(e)
                pass

        def getusersettings(chkkey):

            try:

                url = "{}".format(settings.api_url)
                headers = {'Content-type': 'application/json'}

                r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                for key in r.json():

                    ts3id = key['ts3_identity']
                    settings = key['settings']

                    if ts3id == chkkey:
                        return settings
            except TypeError as e:
                print(e)

        def usersettingsadd(ts3iuid):

            try:
                username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=ts3iuid)
                print(userid, default_settings)
                url = "{}".format(settings.api_url) + '{}'.format(userid)
                r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                settings = r1.json()["settings"]
                settings["notify"] = {}
                url = "{}".format(settings.api_url) + '{}'.format(userid)
                payload = {"settings": json.dumps(settings)}
                r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                print(r.status_code)
                return  r.status_code
            except TypeError as e:
                print(e)

        def ts3connect(sender, event, ts3iuid):

            try:
                found = False

                url = "{}".format(settings.api_url)
                headers = {'Content-type': 'application/json'}
                r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                for user in r.json():
                    if user["ts3id"] == ts3iuid:
                        print("User found ignoring")
                        found = True
                        break


                if found is False:
                    headers = {'Content-type': 'application/json'}
                    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
                    activation_key = hashlib.sha1(salt.encode('utf-8') + str(ts3iuid).encode('utf-8')).hexdigest()
                    a = datetime.datetime.today()
                    b = a + datetime.timedelta(0, 300)  # days, seconds, then other fields.
                    url = 'https://theunlighted.io/api/ts3/'
                    payload = {"ts3id": ts3iuid, "activation_key": activation_key, "key_expires": str(b).replace(" ", "T")}
                    r = requests.post(url, headers=headers, data=json.dumps(payload), auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                    print(r.text)

                    return activation_key

                if found:
                    url = "{}".format(settings.api_url)
                    headers = {'Content-type': 'application/json'}
                    r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                    for user in r.json():
                        if user["ts3id"] == ts3iuid:
                            return user["activation_key"]
            except TypeError as e:
                print(e)

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
                username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=ts3iuid)
                print(userid, default_settings)
                url = "{}".format(settings.api_url) + '{}'.format(userid)
                r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                settings = r1.json()["settings"]
                settings["opts"] = {}
                url = "{}".format(settings.api_url) + '{}'.format(userid)
                payload = {"settings": json.dumps(settings)}
                r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                print(r.status_code)

                return  r.status_code
            except TypeError as e:
                print(e)

        def activateacc(sender, event, cliuid, linkkey, clid):
            try:
                username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=linkkey)

                conns = ""

                for client in ts3conn.clientinfo(clid=clid):
                    conns = int(client['client_totalconnections'])

                def ts3activated():
                    url = "{}".format(settings.api_url) + '{}'.format(userid)
                    r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                    oldsettings = r1.json()["settings"]
                    try:
                        ts3set = oldsettings["teamspeak"]
                    except KeyError:
                        return False
                    if ts3set['activated']:
                        return True
                    else:
                        return False

                if ts3activated() == False:
                    url = "{}".format(settings.api_url) + '{}'.format(userid)
                    r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                    r1.json()["settings"] = {"settings": {},"notify": {}}
                    print(r1.json()["settings"])
                    oldsettings = r1.json()["settings"]
                    oldsettings["teamspeak"] = {"activated": True}
                    for info in ts3conn.clientinfo(clid=event.parsed[0]['invokerid']):
                        oldsettings["teamspeak"]["avatar"] = info["client_base64HashClientUID"]
                    print(oldsettings)
                    url = "{}".format(settings.api_url) + '{}'.format(userid)
                    payload = {'link_key': "{}".format(uuid.uuid4()),'ts3_identity': "{}".format(cliuid), "settings": json.dumps(oldsettings)}
                    r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                    print(r.text)
                    print('{0}: {1} linked their account'.format(r.status_code, username))
                    Functions.addpoints(cliuid=cliuid, addpnt=50)
                    ts3conn.sendtextmessage(targetmode=1, target=Functions.getclinfomsg(sender, event)[3], msg="Account linked to TS3 user, [color=red]{0}[/color] you now have [color=blue]{1}[/color] points and access to commands!".format(username, 50 + conns))
                    try:
                        ts3conn.servergroupaddclient(sgid=111, cldbid=Functions.getclinfomsg(sender, event)[4])
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2561":
                            pass
                if ts3activated() == True:
                    url = "{}".format(settings.api_url) + '{}'.format(userid)
                    oldsettings = r1.json()["settings"]
                    oldsettings["teamspeak"] = {"activated": True}
                    for info in ts3conn.clientinfo(clid=event.parsed[0]['invokerid']):
                        oldsettings["teamspeak"] = {"avatar": info["client_base64HashClientUID"]}
                    payload = {'link_key': "{}".format(uuid.uuid4()), 'ts3_identity': "{}".format(cliuid)}

                    r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                    print(r.status_code)
                    ts3conn.sendtextmessage(targetmode=1, target=Functions.getclinfomsg(sender, event)[3], msg="TS3 user updated. Link key updated (Check website for new code).")
                print(r.json())
            except TypeError as e:
                print("{} attempted to activate an account.".format(cliuid))
                ts3conn.sendtextmessage(targetmode=1, target=Functions.getclinfomsg(sender, event)[3], msg="\n[color=red]Account Activation code not found..[/color]\nTry again with a correctly typed code.")


        def addpoints(cliuid, addpnt):
            username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=cliuid)
            url = "{}".format(settings.api_url) + '{}'.format(userid)
            payload = {'points': points + addpnt}
            r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
            print('{0}: {1} earned {2} points'.format(r.status_code, username, addpnt))

        def clientdbinfo(sender, event):
            cliuid = event.parsed[0]['invokeruid']
            print(cliuid)
            def cliuidtodbid():
                for client in ts3conn.clientgetdbidfromuid(cluid="{}".format(cliuid)):
                    return (client)['cldbid']

            for client in ts3conn.clientdbinfo(cldbid=cliuidtodbid()):
                return (client)

        def levergroupassign(sender, event, points):
            level1 = 2
            level2 = 3
            level3 = 4
            level4 = 5
            level5 = 6
            clidbid = Functions.getclinfoid(sender, event)[4]
            try:
                if int(points) <= 500:
                    # if groups[0] == ''.format(level1 or level2 or level3):
                    try:
                        ts3conn.servergroupaddclient(sgid=118, cldbid=clidbid)
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2561":
                            pass
                    groups = [114, 115, 116, 117, 113]
                    for group in groups:
                        try:
                            ts3conn.servergroupdelclient(sgid=group, cldbid=clidbid)
                        except ts3.query.TS3QueryError as err:
                            if err.resp.error["id"] != "2563":
                                continue
                if int(points) >= 500 and int(points) < 1000:
                    # if groups[0] == ''.format(level1 or level2 or level3):
                    try:
                        ts3conn.servergroupaddclient(sgid=113, cldbid=clidbid)
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2561":
                            pass
                    groups = [114, 115, 116, 117, 118]
                    for group in groups:
                        try:
                            ts3conn.servergroupdelclient(sgid=group, cldbid=clidbid)
                        except ts3.query.TS3QueryError as err:
                            if err.resp.error["id"] != "2563":
                                continue

                if int(points) >= 1000 and int(points) < 1500:
                    # if groups[0] == ''.format(level1 or level2 or level3):
                    try:
                        ts3conn.servergroupaddclient(sgid=114, cldbid=clidbid)
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2561":
                            pass
                    groups = [113, 115, 116, 117, 118]
                    for group in groups:
                        try:
                            ts3conn.servergroupdelclient(sgid=group, cldbid=clidbid)
                        except ts3.query.TS3QueryError as err:
                            if err.resp.error["id"] != "2563":
                                continue

                if int(points) >= 1500 and int(points) < 2250:
                    # if groups[0] == ''.format(level1 or level2 or level3):
                    try:
                        ts3conn.servergroupaddclient(sgid=115, cldbid=clidbid)
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2561":
                            pass
                    groups = [113, 114, 116, 117, 118]
                    for group in groups:
                        try:
                            ts3conn.servergroupdelclient(sgid=group, cldbid=clidbid)
                        except ts3.query.TS3QueryError as err:
                            if err.resp.error["id"] != "2563":
                                continue

                if int(points) >= 2250 and int(points) < 3500:
                    # if groups[0] == ''.format(level1 or level2 or level3):
                    try:
                        ts3conn.servergroupaddclient(sgid=116, cldbid=clidbid)
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2561":
                            pass
                    groups = [113, 115, 114, 117, 118]
                    for group in groups:
                        try:
                            ts3conn.servergroupdelclient(sgid=group, cldbid=clidbid)
                        except ts3.query.TS3QueryError as err:
                            if err.resp.error["id"] != "2563":
                                continue

                if int(points) >= 3500 and int(points) < 5000:
                    # if groups[0] == ''.format(level1 or level2 or level3):
                    try:
                        ts3conn.servergroupaddclient(sgid=117, cldbid=clidbid)
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2561":
                            pass
                    groups = [113, 115, 116, 114, 118]
                    for group in groups:
                        try:
                            ts3conn.servergroupdelclient(sgid=group, cldbid=clidbid)
                        except ts3.query.TS3QueryError as err:
                            if err.resp.error["id"] != "2563":
                                continue

            except ts3.query.TS3QueryError as err:
                if err.resp.error["id"] != "2563":
                    pass

        def requestrin(sender, event):
            if event.event == 'notifyclientmoved':
                if event.parsed[0]['ctid'] == '4':
                    ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'], msg="Rin~Sama at your service! o7")

            # if event.event == 'notifycliententerview':
            #     userinfo = Functions.checkusers(chkkey=event.parsed[0]['client_unique_identifier'])
            #     if event.parsed[0]["client_type"] == "1":
            #         pass
            #     if userinfo:
            #         pass
            #     if userinfo is False:
            #         Functions.ts3connect(sender, event, ts3iuid=event.parsed[0]["client_unique_identifier"])



        def movetochan(sender, event):
            ts3conn.clientmove(cid=Functions.getclinfomsg(sender, event)[0], clid=me)

        def movebackchan(sender, event):
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

        def welcomemsg(sender, event):

            try:
                # mutelist = pickle.load(open("mutedlist.p", "rb"))

                if event.event == 'notifycliententerview':
                    if event.parsed[0]["client_type"] == "1":
                        pass
                        # else:
                        #     for client in ts3conn.clientinfo(clid=event.parsed[0]["clid"]):
                        #         for ip in mutelist:
                        #             if client['connection_client_ip'] == ip:
                        #                 print(client['client_database_id'])
                        #                 ts3conn.servergroupaddclient(sgid=22, cldbid=client['client_database_id'])

                if event.event == 'notifycliententerview':
                    userinfo = Functions.checkusers(chkkey=event.parsed[0]['client_unique_identifier'])
                    if event.parsed[0]["client_type"] == "1":
                        pass
                    else:
                        try:
                            if userinfo:
                                cliuid = event.parsed[0]['client_unique_identifier']
                                username, userid, email, ts3id, points, linkkey = Functions.checkusers(
                                    chkkey=cliuid)
                                Functions.addpoints(cliuid=cliuid, addpnt=1)
                                Functions.levergroupassign(sender, event, points)
                                if len(str(points)) < 4:
                                    points = "{} [color=#333399]points![/color]  ".format(points)
                                else:
                                    points = "{} [color=#333399]points![/color] ".format(points)
                                ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'],
                                                            msg=reply['welcomemsgreg'].format(username, points,
                                                                                              ))

                            if userinfo is None:
                                try:


                                    tsconnecto = Functions.ts3connect(sender, event,
                                                         ts3iuid=event.parsed[0]["client_unique_identifier"])
                                    ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'],
                                                            msg=reply['welcomenonreg'].format(tsconnecto))
                                except ts3.query.TS3QueryError as err:
                                    if err.resp.error["id"] != "770":
                                        print("Ignoring user in channel...")
                        except KeyboardInterrupt:
                            print('No duh')
            except TypeError as e:
                print(e)

            except KeyError as e:
                print(e)

    class Commands:

        def commands(sender, event):
            notifytextmessage = event.event == 'notifytextmessage'

            try:
                if notifytextmessage:
                    clid = event.parsed[0]['invokerid']
                    cliuid = event.parsed[0]['invokeruid']
                    if event.parsed[0]["invokeruid"] == "serveradmin":
                        return
                    msg = event.parsed[0]['msg']
                    # get_command(msg)
                    #
                    # def get_command(command):
                    #
                    #     registered_commands = {
                    #         '!test1': ts3conn.sendtextmessage(targetmode=1,
                    #                                  target=clid,
                    #                                    msg="Works!")
                    #         }
                    #     if command in registered_commands.keys():
                    #         registered_commands[command]()
                    if msg.startswith('!'):
                        if msg == '!link':
                            clid = event.parsed[0]['invokerid']
                            cliuid = event.parsed[0]['invokeruid']
                            activatekey = event.parsed[0]['msg'][6:]
                            # Functions.activateacc(sender, event, cliuid=cliuid, linkkey=activatekey, clid=clid)

                        # userinfo = Functions.checkusers(chkkey=event.parsed[0]['invokeruid'])
                        # if userinfo is None:
                        #         try:
                        #             ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['invokerid'], msg="[color=red]Access denied[/color]. You are not registered.")
                        #             return
                        #         except ts3.query.TS3QueryError as err:
                        #             if err.resp.error["id"] != "770":
                        #                 print("Ignoring user in channel...")

                        if msg == '!love':
                            Commands.love(sender, event)
                        if msg.startswith('!joke'):
                            print(BASE_DIR)
                            with open(BASE_DIR + '/jokes.txt') as f:
                                joke = random.choice(list(f))
                                ts3conn.sendtextmessage(targetmode=2,
                                                target=Functions.getclinfomsg(sender, event)[0],
                                                msg="{}".format(joke))
                                ts3conn.sendtextmessage(targetmode=1,
                                                    target=event.parsed[0]['invokerid'],
                                                    msg="{}".format(joke))
                        if msg == '!myprofile':
                            Commands.myprofile(sender, event)
                        if msg.startswith('!findani') or msg.startswith('!FINDANI'):
                            animesearch = msg[9:]
                            if animesearch == "":
                                ts3conn.sendtextmessage(targetmode=1,
                                                    target=clid,
                                                    msg="Incorrect use of command.")
                            else:
                                Commands.searchanime(sender, event, search=animesearch)
                        if msg == '!kawaii':
                            r = praw.Reddit(user_agent='my_cool_application')
                            submissions = r.get_subreddit('awwnime').get_new()
                            list_of_urls = []
                            for x in submissions:
                                list_of_urls.append(x.url)


                            ts3conn.sendtextmessage(targetmode=2,
                                                target=Functions.getclinfomsg(sender, event)[0],
                                                msg="[url]{}[/url]".format(random.choice(list_of_urls)))


                        if msg.startswith('!aninfo') or msg.startswith('!ANINFO'):
                            animesearch = msg[8:]
                            if animesearch == "":
                                ts3conn.sendtextmessage(targetmode=1,
                                                        target=clid,
                                                        msg="Incorrect use of command.")
                            else:
                                Commands.animeinfo(sender, event, search=animesearch)
                        if msg.startswith('!listadd'):
                            try:
                                newaniadd = int(msg[9:])
                                Commands.addnotify(sender, event, key=newaniadd)
                            except ValueError:
                                ts3conn.sendtextmessage(targetmode=1,
                                                    target=clid,
                                                    msg="Incorrect use of command.")
                                return


                        if msg.startswith('!listdel'):
                            delani = int(msg[9:])
                            print(delani)
                            Commands.removenotify(sender, event, key=delani)
                        if msg == '!mynlist':
                            Commands.sendlist(sender, event)
                        if msg == '!alllists':
                            clisettings = pickle.load(open("save.p", "rb"))
                            print(clisettings)
                        if msg == '!test2':
                            Commands.removegroup(sender, event)
                        if msg.startswith('!mute') or msg.startswith('!MUTE'):
                            userip = msg[5:]
                            Commands.muteuser(sender, event, userip=userip)
                        if msg.startswith('!mp') or msg.startswith('!MP'):
                            msg = msg[3:]
                            Commands.masspoke(sender, event, msg=msg)
                        if msg.startswith('!optin') or msg.startswith('!OPTIN'):
                            key = msg[7:]
                            Commands.optin(sender, event, key=key)
                        if msg.startswith('!test'):
                        #     Commands.whirlpool(ts3conn)
                            thing = {}
                            dictlist = ()
                            # for user in ts3conn.clientgetids(cluid=cliuid):
                            #     print(user["clid"])
                            a = datetime.datetime.today()
                            b = a + datetime.timedelta(0, 300)  # days, seconds, then other fields.
                            print(str(b).replace(" ", "T"))
                        # Commands.friends(sender, event)
                        # AnimeNotifier.checkusers()
            except KeyError as e:
                print(e)
                pass

        def removegroup(sender, event):
            for client in ts3conn.clientlist():
                clid = client['clid']
                if client['client_type'] == 1:
                    pass
                print(client)
                for info in ts3conn.clientinfo(clid=client['clid']):
                    print(info)
                    try:
                        if '81' and '104' and '87' in info['client_servergroups']:

                            ts3conn.servergroupdelclient(sgid=104, cldbid=info['client_database_id'])
                            ts3conn.servergroupdelclient(sgid=81, cldbid=info['client_database_id'])
                            # ts3conn.clientkick(reasonid=5, reasonmsg="No.", clid=clid)
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "2663":
                            continue


        def masspoke(sender, event, msg):

            for client in ts3conn.clientlist():
                if client['client_type'] == '1' or client['client_database_id'] == '1':
                    continue
                else:
                    ts3conn.clientpoke(msg="""{} ~{}""".format(msg, event.parsed[0]['invokername']), clid=client['clid'])

        def muteuser(sender, event, userip):
            clid = event.parsed[0]['invokerid']
            mutelist = pickle.load(open("mutedlist.p", "rb"))
            if userip not in mutelist:
                pickle.dump(userip, open("save.p", "wb"))
                ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="Done. {}".format(mutelist))

        def love(sender, event):
            msg = event.parsed[0]['msg']
            clid = event.parsed[0]['invokerid']
            cliuid = event.parsed[0]['invokeruid']
            cliname = event.parsed[0]['invokername']
            lovesay = list(sayings['love'])
            ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="{}".format(str(random.choice(lovesay)).format(cliname))
                                    )
            try:
                try:
                    Functions.movetochan(sender, event)

                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "770":
                        print("Ignoring user in channel...")
                ts3conn.sendtextmessage(targetmode=2,
                                        target=Functions.getclinfomsg(sender, event)[0],
                                        msg="{}".format(str(random.choice(lovesay)).format(cliname)))
                Functions.movebackchan(sender, event)
            except ts3.query.TS3QueryError as err:
                if err.resp.error["id"] != "770":
                    print("Ignoring user in channel...")
        def optin(sender, event, key):
            cliuid = event.parsed[0]['invokeruid']
            username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=cliuid)
            try:
                url = "{}".format(settings.api_url) + '{}'.format(userid)
                r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                oldsettings = r1.json()["settings"]
                opts = oldsettings["opts"]
            except KeyError:
                ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['invokerid'], msg="No Opt config found. Creating one...")
                Functions.useroptsadd(ts3iuid=ts3id)
                ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['invokerid'], msg="Done.")
            try:
                url = "{}".format(settings.api_url) + '{}'.format(userid)
                r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                oldsettings = r1.json()["settings"]
                opts = oldsettings["opts"]
                opts['{}'.format(key)] = True
                url = "{}".format(settings.api_url) + '{}'.format(userid)
                payload = {"settings": json.dumps(oldsettings)}
                r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                print(r.status_code)
                ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['invokerid'], msg="Optted in for Anime Notifications!")
                return  r.status_code
            except TypeError as e:
                print(e)
        def myprofile(sender, event):
            msg = event.parsed[0]['msg']
            clid = event.parsed[0]['invokerid']
            cliuid = event.parsed[0]['invokeruid']
            cliname = event.parsed[0]['invokername']
            userinfo = Functions.checkusers(chkkey=cliuid)
            ts3conn.sendtextmessage(targetmode=1, target=clid, msg="Please wait while I fetch your info....")
            try:
                if userinfo:
                    username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=cliuid)
                    ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg=reply['clistats'].format(username, email, ts3id, points)
                                            )
                if userinfo is None:
                    ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="You are not registered."
                                            )
            except TypeError as e:
                print(e)

        def friends(sender, event):
            clid = event.parsed[0]['clid']
            cliuid = event.parsed[0]['client_unique_identifier']
            userinfo = Functions.checkusers(chkkey=cliuid)
            friendlist =""
            try:
                if userinfo:
                    username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=cliuid)
                    try:
                        url = 'https://theunlighted.io/api/friends'
                        r = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                        for key in r.json():
                            touser = key['to_user']
                            fromuser = key['from_user']
                            if "https://theunlighted.io/api/users/{}/".format(userid) == touser:
                                url = fromuser
                                r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                                try:
                                    for info in ts3conn.clientgetids(cluid=r1.json()['ts3_identity']):
                                        friendlist = friendlist + " | " + r1.json()['display_name'] + " Online"
                                except ts3.query.TS3QueryError as err:
                                    print(r1.json()['display_name'] + " Offline")
                                    if err.resp.error["id"] != "1281":
                                        continue
                        if friendlist == "":
                            return "No friends online"

                    except None:
                        return "You have no friends added"

                return friendlist
            except TypeError as e:
                print(e)
        def searchanime(sender, event, search):
            msg = event.parsed[0]['msg']
            clid = event.parsed[0]['invokerid']
            cliuid = event.parsed[0]['invokeruid']
            cliname = event.parsed[0]['invokername']
            ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="Searching for {}...".format(search))
            url = 'https://anilist.co/api/anime/search/{}'.format(search)
            params = {'access_token': '{}'.format(Functions.gettoken())}
            r = requests.get(url, params=params)
            try:
                ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="There are {0} matches!".format(len(r.json()))
                                    )
            except ValueError:
                ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="There are 0 matches!"
                                        )
                pass

            def get_all():

                x = 1
                try:
                    for anime in r.json():
                        print(r.json())
                        title = anime['title_english']
                        idani = anime['id']
                        status = anime['airing_status']
                        ts3conn.sendtextmessage(targetmode=2,
                                                target=Functions.getclinfomsg(sender, event)[0],
                                                msg="{0} - [color=blue]Title:[/color] [color=green]{1}[/color], [color=blue]Status:[/color] [color=darkorange]{2}[/color], [color=blue]ID:[/color] {3}".format(
                                                    x, title, status, idani))

                        ts3conn.sendtextmessage(targetmode=1,
                                                target=clid,
                                                msg="{0} - [color=blue]Title:[/color] [color=green]{1}[/color], [color=blue]Status:[/color] [color=darkorange]{2}[/color], [color=blue]ID:[/color] {3}".format(x, title, status, idani))
                        x += 1
                except ValueError:
                    ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="No matches found")
            get_all()

        def animeinfo(sender, event, search):
            msg = event.parsed[0]['msg']
            clid = event.parsed[0]['invokerid']
            cliuid = event.parsed[0]['invokeruid']
            cliname = event.parsed[0]['invokername']
            url = 'https://anilist.co/api/anime/{}'.format(search)
            params = {'access_token': '{}'.format(Functions.gettoken())}
            r = requests.get(url, params=params)
            print(r.json())
            title = r.json()['title_english']
            idani = r.json()['id']
            status = r.json()['airing_status']
            s = r.json()["description"]
            lim = 500
            ts3conn.sendtextmessage(targetmode=1,
                            target=clid,
                            msg="[color=blue]Title:[/color] [color=green]{0}[/color], [color=blue]Status:[/color] [color=darkorange]{1}[/color]".format(
                                title, status))
            ts3conn.sendtextmessage(targetmode=2,
                                    target=Functions.getclinfomsg(sender, event)[0],
                                    msg="[color=blue]Decription:[/color]")
            for s in s.split("\n"):
                w = 0
                l = []
                for d in s.split():
                    if w + len(d) + 1 <= lim:
                        l.append(d)
                        w += len(d) + 1
                    else:
                        print(" ".join(l))
                        ts3conn.sendtextmessage(targetmode=2,
                                target=Functions.getclinfomsg(sender, event)[0],
                                msg="[color=green]{0}[/color]".format(" ".join(l)))
                        l = [d]
                        w = len(d)
                if (len(l)): print(" ".join(l))
            # ts3conn.sendtextmessage(targetmode=1,
            #                     target=clid,
            #                     msg="{}".format(textwrap.fill(s, 500))
            #                     )


            # ts3conn.sendtextmessage(targetmode=1,
            #                 target=clid,
            #                 msg="[color=blue]Title:[/color] [color=green]{0}[/color], [color=blue]Status:[/color] [color=darkorange]{1}[/color], [color=blue]ID:[/color] {2}".format(
            #                     title, status, textwrap.fill(s, 500)))



            if clid != 0:
                pass

        def addnotify(sender, event, key):
            msg = event.parsed[0]['msg']
            clid = event.parsed[0]['invokerid']
            cliuid = event.parsed[0]['invokeruid']
            cliname = event.parsed[0]['invokername']
            clisettings = Functions.getusersettings(chkkey=event.parsed[0]['invokeruid'])
            username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=cliuid)
            ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="[color=#ff6633]Please wait while I check everything....[/color]")
            try:
                if clisettings["notify"] == {}:
                    ts3conn.sendtextmessage(targetmode=1,
                                                target=clid,
                                                msg="You do not seem to have a notification config.. Creating one...")
                    Functions.usersettingsadd(ts3iuid=cliuid)
                    ts3conn.sendtextmessage(targetmode=1,
                                                target=clid,
                                                msg="Done.")
            except:
                ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="You do not seem to have a notification config.. Creating one...")
                Functions.usersettingsadd(ts3iuid=cliuid)
                ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="Done.")

            if type(key) is not int:
                ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="[color=red]{} is not a valid [color=blue]ID[/color]. Please get the ID from the [color=green]!findani[/color] command![/color]".format(key))
                return
            def check_anime_exists(key):
                url = 'https://anilist.co/api/anime/{}'.format(key)
                params = {'access_token': '{}'.format(Functions.gettoken())}
                results = requests.get(url, params=params)
                if results.json():
                    return True
                if results.json() is None:
                    return None
            def get_anime_info(key):
                url = 'https://anilist.co/api/anime/{}'.format(key)
                params = {'access_token': '{}'.format(Functions.gettoken())}
                results = requests.get(url, params=params)
                try:
                    if results.json()['airing']:
                        print(results.json()['airing'])
                        return results.json()['title_english'], results.json()['airing']

                except KeyError:
                    return None
            try:
                title, airingtime = get_anime_info(key=key)
            except TypeError:
                ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="Looks like this anime has ended. Too bad... :(")
                return
            if check_anime_exists(key=key) is True:
                if airingtime is None:
                   ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="That is not a currently airing anime, please choose an airing anime")

                if airingtime:
                    def addaninotify():
                        try:
                            url = "{}".format(settings.api_url) + '{}'.format(userid)
                            r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                            oldsettings = r1.json()["settings"]
                            notify = oldsettings["notify"]
                            notify['{}'.format(key)] = title
                            url = "{}".format(settings.api_url) + '{}'.format(userid)
                            payload = {"settings": json.dumps(oldsettings)}
                            r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                            return  r.status_code
                        except TypeError as e:
                            print(e)
                        clisettings['notify']['{}'.format(key)] = airingtime['countdown']
                    addaninotify()
                    def convert_time(a):
                        m, s = divmod(a, 60)
                        h, m = divmod(m, 60)
                        d, h = divmod(h, 24)
                        return "{0} releases in {1} days {2} hours {3} minutes {4} seconds".format(title, d, h, m, s)
                    ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="[color=green]{0}[/color] added to list. [color=blue]{1}[/color]".format(title, convert_time(a=airingtime['countdown'])))
                    print(clisettings)
        # def removenotify(sender, event, key):
        #     msg = event.parsed[0]['msg']
        #     clid = event.parsed[0]['invokerid']
        #     cliuid = event.parsed[0]['invokeruid']
        #     cliname = event.parsed[0]['invokername']
        #     clisettings = Functions.getusersettings(chkkey=event.parsed[0]['invokeruid'])
        #     username, userid, email, ts3id, points, linkkey = Functions.checkusers(chkkey=cliuid)
        #     try:
        #         url = "{}".format(settings.api_url) + '{}'.format(userid)
        #         r1 = requests.get(url, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
        #         oldsettings = r1.json()["settings"]
        #         notify = json.dumps(oldsettings["notify"])
        #
        #         url = "{}".format(settings.api_url) + '{}'.format(userid)
        #         payload = {"settings": json.dumps(dump)}
        #         r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
        #         return  r.status_code
        #     except TypeError as e:
        #         print(e)
        #     print("j")
        def sendlist(sender, event):
            clid = event.parsed[0]['invokerid']
            clisettings = Functions.getusersettings(chkkey=event.parsed[0]['invokeruid'])
            listtext = ""
            cliuid = event.parsed[0]['invokeruid']
            ts3conn.sendtextmessage(targetmode=1, target=clid, msg="Please wait while I fetch your info....")
            def get_anime_info(key):
                url = 'https://anilist.co/api/anime/{}'.format(key)
                params = {'access_token': '{}'.format(Functions.gettoken())}
                results = requests.get(url, params=params)
                try:
                    if results.json()['airing']:
                        print(results.json()['airing'])
                        return results.json()['title_english'], results.json()['airing']

                except KeyError:
                    return None
                except TypeError:
                    ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="Looks like this anime has ended. Too bad... :(")
                return

            if clisettings == {}:
                ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="You do not seem to have a notification config.. Creating one...")
                Functions.usersettingsadd(ts3iuid=cliuid)
                ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="Done. You can add anime by using !search anime then adding the ID to !nadd ID")
                return
            if clisettings["notify"] == {}:
                ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="You have no Anime added to your notification list...")
                return

            try:
                anime = clisettings['notify'].items()
                for k, i in anime:
                    try:
                        title, airingtime = get_anime_info(key=k)
                    except TypeError:
                        continue
                    try:
                        next_episode = airingtime['next_episode']
                        airingtime = airingtime['countdown']

                    except TypeError:
                        ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="[color=green]{}[/color] [color=orange]has ended.[/color]".format(title))
                        continue
                    def convert_time(a):
                        m, s = divmod(a, 60)
                        h, m = divmod(m, 60)
                        d, h = divmod(h, 24)
                        return "{0} days {1} hours {2} minutes {3} seconds till next episode.".format(d, h, m, s)
                    c = '[color=green]{}[/color]'.format(title) + ': ' + '[color=blue]Episode {} will air in[/color] '.format(next_episode) + '[color=blue]{}[/color]'.format(convert_time(a=airingtime))
                    listtext = listtext + c + '\n'
                ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="\n[B][U]Anime List[/U][/B]\n{}".format(listtext))
            except KeyError as e:
                print(e)
        def whirlpool(ts3conn, duration=10, relax_time=0.5):
            """
            Moves all clients randomly in other channels for *duration* seconds.
            After the whirpool event, all clients will be in the same channel as
            before. Between the whirlpool cycles, the programm will sleep for
            *relax_time* seconds.
            """
            # Countdown till whirlpool
            for i in range(5, 0, -1):
                ts3conn.sendtextmessage(
                    targetmode=3,
                    target=0, msg="Whirpool in {}s".format(i))
                time.sleep(1)

            # Fetch the clientlist and the channellist.
            clientlist = ts3conn.clientlist()
            channellist = ts3conn.channellist()

            # Ignore query clients
            clientlist = [client for client in clientlist \
                          if client["client_type"] != "1"]

            # Whirpool with one channel or no users is boring.
            if len(channellist) == 1 or not clientlist:
                return None

            # We need this try-final construct to make sure, that all
            # clients will be in the same channel at the end of the
            # whirlpool as to the beginning.
            try:
                end_time = time.time() + duration
                while end_time > time.time():
                    for client in clientlist:
                        clid = client["clid"]
                        cid = random.choice(channellist)["cid"]
                        try:
                            ts3conn.clientmove(clid=clid, cid=cid)
                        except ts3.query.TS3QueryError as err:
                            # Only ignore 'already member of channel error'
                            if err.resp.error["id"] != "770":
                                raise
                            if err.resp.error["id"] != "2568":
                                raise
                    time.sleep(relax_time)
            finally:
                # Move all clients back
                list2 = [13, 38, 52, 37, 50, 39, 58, 57, 55, 53, 54, 34]
                for client in clientlist:
                    try:
                        for user in list2:
                            if client["clid"] == user:
                                continue
                        ts3conn.clientmove(clid=client["clid"], cid=client["cid"])
                    except ts3.query.TS3QueryError as err:
                        if err.resp.error["id"] != "770":
                            raise
                        if err.resp.error["id"] != "2568":
                            raise
            return None
    class AnimeNotifier:

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
            params = {'access_token': '{}'.format(AnimeNotifier.gettoken())}
            r = requests.get(url, params=params)
            return r.json()['title_english'], r.json()['airing']['countdown']

        def checkusers():

            try:

                url = "{}".format(settings.api_url)
                headers = {'Content-type': 'application/json'}
                r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                opted = 0
                unopted = 0
                for key in r.json():
                    try:
                        settings = key['settings']['opts']
                        if settings['Aninotify'] == True:
                            AnimeNotifier.check_anime_times(ts3uid=key["ts3_identity"])
                            opted += 1
                    except KeyError:
                        unopted += 1
                        continue
                print("Aninotify run results: {} users notified | {} users not opted.".format(opted, unopted))
            except TypeError as e:
                print(e)

        def check_anime_times(ts3uid):
            clid = int(1)
            for client in ts3conn.clientgetids(cluid="{}".format(ts3uid)):
                clid = client["clid"]
            listtext = ""
            clisettings = Functions.getusersettings(chkkey=ts3uid)
            for anime, title in clisettings['notify'].items():
                title, a = AnimeNotifier.checkrelease(search=anime)
                m, s = divmod(a, 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                c = '[color=green]{}[/color]'.format(title) + ': '  + '[color=blue]{}[/color]'.format("{0} releases in {1} days {2} hours {3} minutes {4} seconds".format(title, d, h, m, s))
                listtext = listtext + c + '\n'
            ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="\n[B][U]Anime List[/U][/B]\n{}".format(listtext))


    def my_event_handler(sender, event):
            """
            *sender* is the TS3Connection instance, that received the event.

            *event* is a ts3.response.TS3Event instance, that contains the name
            of the event and the data.
            """
            print("Event:")
            print("  sender:", sender)
            print("  event.event:", event.event)
            print("  event.parsed:", event.parsed)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("""
    ___     __                 ___
   F _ ",   LJ   _ ___   /\/] F __".   ___ _    _ _____      ___ _
  J `-'(|       J '__ J /   /J (___|  F __` L  J '_  _ `,   F __` L
  |  _  L   FJ  | |__| |L/\//J\___ \ | |--| |  | |_||_| |  | |--| |
  F |_\  L J  L F L  J JL/\/.--___) \F L__J J  F L LJ J J  F L__J J
 J__| \\__LJ__LJ__L  J__L   J\______J\____,__LJ__L LJ J__LJ\____,__L
 |__|  J__||__||__L  J__|    J______FJ____,__F|__L LJ J__| J____,__F

    """)
    #
    # def centrigoserv(chann, data):
    #     client = Client("https://theunlighted.io:8432/api/", "theunlighted", "3c88faac-7e6e-42ca-6d97-04ce1f969a25")
    #     params = {
    #         "channel": chann,
    #         "data": {
    #             "input": data
    #         }
    #     }
    #     client.add("publish", params)
    #     result, error = client.send()

    try:
        with ts3.query.TS3Connection("{}".format(settings.ts_url)) as ts3conn:

            ts3conn.login(client_login_name=USER, client_login_password=PASS)
            ts3conn.use(sid=1)
       

            me = ts3conn.whoami()[0]['client_id']
            ts3conn.clientupdate(CLIENT_NICKNAME='Rin~Sama v0.9.1')
            # Move the bot to the channel
            ts3conn.clientmove(cid=209, clid=me)
            # Register notifs and handle in new thread
            ts3conn.servernotifyregister(event="server")
            ts3conn.servernotifyregister(event="textserver")
            ts3conn.servernotifyregister(event="textprivate")
            ts3conn.servernotifyregister(event="textchannel")
            ts3conn.servernotifyregister(event="channel", id_=4)
            event = ts3conn.wait_for_event()
            print('Rin~Sama Operational')
           
            input('> ')
    except KeyError as e:
        print(e)
        sys.exit()
# Main
# ------------------------------------------------

USER = "serveradmin"
PASS = "{}".format(settings.password)

if __name__ == "__main__":
    main()
