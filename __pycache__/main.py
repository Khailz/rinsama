# # --------------------------------------------------------------------------------
# # Rin~Sama Alpha v0.7
# # ---------------------
# # Functions:
# #
# # connect to theunlighted.com teamspeak ?
# # Connect to beta.theunlighted.com django api or DB ?
# # Authenticate user account on website with teamspeak ?
# # AniList Search Support ?
# # MAL account connection
# # Point system both website and Rin~Sama ?
# # Create requested channels "After donation"
# # Purchase Bot with Paypal ?
# # IRC type mini games such as history questions, roulette, dice, etc ?
# # Twitch authentication
# # Reward with server groups ?
# # News feature
# # Leaderboards ? sort fo
# # AIML supprt if I can do it :D
# # ---------------------------------------------------------------------------------

# Installed packages in library
import sys, os, time, random, ts3, sqlite3, threading, shlex, copy, \
    re, json, operator, requests, logging, paypalrestsdk, datetime, uuid, \
    pickle, socket

# Other Packages
from Games import trivia
from cent.core import Client
from sayings import reply, sayings
from multiprocessing import Process
from time import sleep, time
from threading import Thread

logging.basicConfig(filename='rinlog.log',level=logging.DEBUG,
        format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

default_settings = {'notify': {}}

class Functions:

    def getclinfomsg(sender, event):
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

    def getclinfoid(sender, event):
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

    def checkusers(chkkey):

        try:

            url = 'http://beta.theunlighted.com/api/users'
            headers = {'Content-type': 'application/json'}

            r = requests.get(url, headers=headers, auth=('khailz', 'mikhail9'))
            for key in r.json():

                email = key['email']
                points = key['points']
                ts3id = key['ts3_identity']
                username = key['username']
                userid = key['id']
                rpgrace = key['rpg_race']
                acckey = key['activation_key']
                groups = key['groups']

                if ts3id == chkkey or acckey == chkkey:
                    return username, userid, email, ts3id, points, rpgrace, acckey, groups
        except TypeError as e:
            print(e)
    def activateacc(sender, event, cliuid, acckey, clid):
        try:
            username, userid, email, ts3id, points, rpgrace, acckey, groups = Functions.checkusers(chkkey=acckey)

            conns = ""

            for client in ts3conn.clientinfo(clid=clid):
                conns = int(client['client_totalconnections'])

            url = 'http://beta.theunlighted.com/api/users/{}/'.format(userid)
            payload = {'ts3_identity': cliuid}
            r = requests.put(url, data=payload, auth=('khailz', 'mikhail9'))
            print('{0}: {1} linked their account'.format(r.status_code, username))
            Functions.addpoints(cliuid=cliuid, addpnt=50)
            ts3conn.sendtextmessage(targetmode=1, target=Functions.getclinfomsg(sender, event)[3], msg="Account Activated [color=red]{0}[/color] you now have [color=blue]{1}[/color] points!".format(username, 50 + conns))
            try:
                ts3conn.servergroupaddclient(sgid=111, cldbid=Functions.getclinfomsg(sender, event)[4])

            except ts3.query.TS3QueryError as err:
                if err.resp.error["id"] != "2561":
                    pass
        except TypeError as e:
            print(e)
            ts3conn.sendtextmessage(targetmode=1, target=Functions.getclinfomsg(sender, event)[3], msg="\n[color=red]Account Activation code not found..[/color]\nTry again with a correctly typed code.")


    def addpoints(cliuid, addpnt):
        username, userid, email, ts3id, points, rpgrace, acckey, groups = Functions.checkusers(chkkey=cliuid)
        url = 'http://beta.theunlighted.com/api/users/{}/'.format(userid)
        payload = {'points': points + addpnt}
        r = requests.put(url, data=payload, auth=('khailz', 'mikhail9'))
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
            if int(points) >= 500 and int(points) < 1000:
                # if groups[0] == 'http://beta.theunlighted.com/api/groups/{}/'.format(level1 or level2 or level3):
                try:
                    ts3conn.servergroupaddclient(sgid=113, cldbid=clidbid)
                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "2561":
                        pass
                ts3conn.servergroupdelclient(sgid=116, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=115, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=114, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=117, cldbid=clidbid)
            if int(points) >= 1000 and int(points) < 1500:
                # if groups[0] == 'http://beta.theunlighted.com/api/groups/{}/'.format(level1 or level2 or level3):
                try:
                    ts3conn.servergroupaddclient(sgid=114, cldbid=clidbid)
                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "2561":
                        pass
                ts3conn.servergroupdelclient(sgid=116, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=115, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=117, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=113, cldbid=clidbid)
            if int(points) >= 1500 and int(points) < 2250:
                # if groups[0] == 'http://beta.theunlighted.com/api/groups/{}/'.format(level1 or level2 or level3):
                try:
                    ts3conn.servergroupaddclient(sgid=115, cldbid=clidbid)
                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "2561":
                        pass
                ts3conn.servergroupdelclient(sgid=116, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=117, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=114, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=113, cldbid=clidbid)
            if int(points) >= 2250 and int(points) < 3500:
                # if groups[0] == 'http://beta.theunlighted.com/api/groups/{}/'.format(level1 or level2 or level3):
                try:
                    ts3conn.servergroupaddclient(sgid=116, cldbid=clidbid)
                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "2561":
                        pass
                ts3conn.servergroupdelclient(sgid=117, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=115, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=114, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=113, cldbid=clidbid)

            if int(points) >= 3500 and int(points) < 5000:
                # if groups[0] == 'http://beta.theunlighted.com/api/groups/{}/'.format(level1 or level2 or level3):
                try:
                    ts3conn.servergroupaddclient(sgid=117, cldbid=clidbid)
                except ts3.query.TS3QueryError as err:
                    if err.resp.error["id"] != "2561":
                        pass
                ts3conn.servergroupdelclient(sgid=116, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=115, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=114, cldbid=clidbid)
                ts3conn.servergroupdelclient(sgid=113, cldbid=clidbid)

        except ts3.query.TS3QueryError as err:
            if err.resp.error["id"] != "2563":
                pass

    def movetochan(sender, event):
        ts3conn.clientmove(cid=Functions.getclinfomsg(sender, event)[0], clid=me)

    def movebackchan(sender, event):
        ts3conn.clientmove(cid=209, clid=me)

    def gettoken():
        url = 'https://anilist.co/api/auth/access_token'

        data = {'grant_type': "client_credentials", 'client_id': 'khailz-2xeuu', 'client_secret': 'I47OnQFEaUBdi11xA6SGgsK6rryj'}

        r = requests.post(url, params=data)


        accessinfo = json.loads(r.text)
        token = accessinfo['access_token']

        # print("Access Granted, access token is " + token)

        return accessinfo['access_token']

    def welcomemsg(sender, event):

        try:
            mutelist = pickle.load(open("mutedlist.p", "rb"))

            if event.event == 'notifycliententerview':
                if event.parsed[0]["client_type"] == "1":
                    pass
                else:
                    for client in ts3conn.clientinfo(clid=event.parsed[0]["clid"]):
                        for ip in mutelist:
                            if client['connection_client_ip'] == ip:
                                print(client['client_database_id'])
                                ts3conn.servergroupaddclient(sgid=22, cldbid=client['client_database_id'])


            if event.event == 'notifycliententerview':
                userinfo = Functions.checkusers(chkkey=event.parsed[0]['client_unique_identifier'])
                if event.parsed[0]["client_type"] == "1":
                            pass
                else:
                    try:
                        if userinfo:
                            cliuid = event.parsed[0]['client_unique_identifier']
                            username, userid, email, ts3id, points, rpgrace, acckey, groups = Functions.checkusers(chkkey=cliuid)
                            Functions.addpoints(cliuid=cliuid, addpnt=1)
                            ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'], msg=reply['welcomemsgreg'].format(username, points))
                            Functions.levergroupassign(sender, event, points)

                        if userinfo is None:
                            try:
                                ts3conn.clientmove(cid=1568, clid=event.parsed[0]['clid'])
                                ts3conn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'], msg=reply['welcomenonreg'])
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

        if notifytextmessage:
            msg = event.parsed[0]['msg']
            if msg.startswith('!activate') or msg.startswith('!ACTIVATE'):
                clid = event.parsed[0]['invokerid']
                cliuid = event.parsed[0]['invokeruid']

                activatekey = event.parsed[0]['msg'][10:]
                Functions.activateacc(sender, event, cliuid=cliuid, acckey=activatekey, clid=clid)

            if msg == '!love':
                Commands.love(sender, event)
            if msg == '!myprofile':
                Commands.myprofile(sender, event)
            if msg.startswith('!findani') or msg.startswith('!FINDANI'):
                animesearch = msg[9:]
                Commands.searchanime(sender, event, search=animesearch)
            if msg.startswith('!listadd'):
                newaniadd = int(msg[9:])
                print(newaniadd)
                Commands.addnotify(sender, event, key=newaniadd)
            if msg == '!mynlist':
                Commands.sendlist(sender, event)
            if msg == '!alllists':
                clisettings = pickle.load(open("save.p", "rb"))
                print(clisettings)
            if msg.startswith('!mute') or msg.startswith('!MUTE'):
                userip = msg[5:]
                Commands.muteuser(sender, event, userip=userip)
            if msg.startswith('!mp') or msg.startswith('!MP'):
                msg = msg[3:]
                Commands.masspoke(sender, event, msg=msg)
            if msg.startswith('!test'):
                Commands.masspoke(sender, event)

    def masspoke(sender, event, msg):

        for client in ts3conn.clientlist():
            if client['client_type'] == '1' or client['client_database_id'] == '1':
                continue
            else:
                ts3conn.clientpoke(msg="{} ~{}".format(msg, event.parsed[0]['invokername']), clid=client['clid'])

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

    def myprofile(sender, event):
        msg = event.parsed[0]['msg']
        clid = event.parsed[0]['invokerid']
        cliuid = event.parsed[0]['invokeruid']
        cliname = event.parsed[0]['invokername']
        userinfo = Functions.checkusers(chkkey=cliuid)
        ts3conn.sendtextmessage(targetmode=1, target=clid, msg="Please wait while I fetch your info....")
        try:
            if userinfo:
                username, userid, email, ts3id, points, rpgrace, acckey, groups = Functions.checkusers(chkkey=cliuid)
                ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg=reply['clistats'].format(username, email, ts3id, points, rpgrace, groups)
                                        )
            if userinfo is None:
                ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="You are not registered."
                                        )
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
        ts3conn.sendtextmessage(targetmode=1,
                                target=clid,
                                msg="There are {0} matches!".format(len(r.json()))
                            )
        def get_all():

            for anime in r.json():
                print(r.json())
                title = anime['title_english']
                idani = anime['id']
                status = anime['airing_status']
                ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="{0} - [color=blue]Title:[/color] [color=green]{1}[/color], [color=blue]Status:[/color] [color=darkorange]{2}[/color], [color=blue]ID:[/color] {3}".format(1, title, status, idani))

        get_all()

        if clid != 0:
            pass

    def addnotify(sender, event, key):
        msg = event.parsed[0]['msg']
        clid = event.parsed[0]['invokerid']
        cliuid = event.parsed[0]['invokeruid']
        cliname = event.parsed[0]['invokername']
        clisettings = pickle.load(open("save.p", "rb"))
        ts3conn.sendtextmessage(targetmode=1,
                                target=clid,
                                msg="[color=#ff6633]Please wait while I check everything....[/color]")
        if cliuid not in clisettings:
            ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="You do not seem to have a notification config.. Creating one...")
            clisettings[cliuid] = default_settings
            pickle.dump(clisettings, open("save.p", "wb"))
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
        title, airingtime = get_anime_info(key=key)
        if check_anime_exists(key=key) is True:
            clisettings = pickle.load(open("save.p", "rb"))
            if cliuid in clisettings:
                setfind = clisettings['{}'.format(cliuid)]
                print(setfind)
                if setfind:
                    if airingtime is None:
                        ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="That is not a currently airing anime, please choose an airing anime")

                    if airingtime:
                        print(airingtime)
                        clisettings['{}'.format(cliuid)]['notify']['{}'.format(key)] = airingtime['countdown']
                        pickle.dump(clisettings, open("save.p", "wb"))
                        def convert_time(a):
                            m, s = divmod(a, 60)
                            h, m = divmod(m, 60)
                            d, h = divmod(h, 24)
                            return "{0} releases in {1} days {2} hours {3} minutes {4} seconds".format(title, d, h, m, s)
                        ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="[color=green]{0}[/color] added to list. [color=blue]{1}[/color]".format(title, convert_time(a=airingtime['countdown'])))
                        print(clisettings)

    def sendlist(sender, event):
        clid = event.parsed[0]['invokerid']
        clisettings = pickle.load(open("save.p", "rb"))
        listtext = ""
        cliuid = event.parsed[0]['invokeruid']
        ts3conn.sendtextmessage(targetmode=1, target=clid, msg="Please wait while I fetch your info....")
        def get_anime_info(key):
            url = 'https://anilist.co/api/anime/{}'.format(key)
            params = {'access_token': '{}'.format(Functions.gettoken())}
            results = requests.get(url, params=params)
            return results.json()['title_english'], results.json()['airing']
        if cliuid not in clisettings:
            ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="You do not seem to have a notification config.. Creating one...")
            clisettings[cliuid] = default_settings
            pickle.dump(clisettings, open("save.p", "wb"))
            ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="Done. You can add anime by using !search anime then adding the ID to !nadd ID")
        if cliuid in clisettings:
            try:
                setfind = clisettings['{}'.format(cliuid)]
                anime = setfind['notify'].items()
                for k, i in anime:
                    title, airingtime = get_anime_info(key=k)
                    try:
                        next_episode = airingtime['next_episode']

                    except TypeError:
                        continue
                    try:
                        print(airingtime)
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
                                        msg="\n{}".format(listtext))
            except KeyError:
                ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                    msg="You have no Anime added to your notification list...")

class AnimeNotifier:

    default_settings = {'notify': {}}

    def __init__(self):
        self.notify_queue  = {}

    def pending_notify(self, cliuid):

        for client in self.notify_queue:
            if client == cliuid:
                return True

    def should_notify(self, cliuid):
        length = time() - self.notify_queue[cliuid]
        if length > 20:
            return True

        return False

    def gettoken(self):
        url = 'https://anilist.co/api/auth/access_token'
        data = {'grant_type': "client_credentials", 'client_id': 'khailz-2xeuu', 'client_secret': 'I47OnQFEaUBdi11xA6SGgsK6rryj'}
        r = requests.post(url, params=data)
        accessinfo = json.loads(r.text)
        token = accessinfo['access_token']
        return accessinfo['access_token']

    def checkrelease(self, search):
        url = 'https://anilist.co/api/anime/{}'.format(search)
        params = {'access_token': '{}'.format(self.gettoken())}
        r = requests.get(url, params=params)
        return r.json()['title_english'], r.json()['airing']['countdown']

    def check_anime_times(self):
        clisettings = pickle.load(open("save.p", "rb"))

        for client in clisettings:
            cliuid = client
            setfind = clisettings['{}'.format(cliuid)]
            print(setfind)
            if setfind:
                print(setfind['notify'])
                for anime, release in setfind['notify'].items():
                    title, a = self.checkrelease(search=anime)
                    m, s = divmod(a, 60)
                    h, m = divmod(m, 60)
                    d, h = divmod(h, 24)
                    print("{0} releases in {1} days {2} hours {3} minutes {4} seconds".format(title, d, h, m, s))

def changlog_instance():

    def change_notify(sender, event):

        try:

            if event.event == 'notifycliententerview':
                if event.parsed[0]["client_type"] == "1":
                    pass
                else:
                    ts3miniconn.sendtextmessage(targetmode=1, target=event.parsed[0]['clid'], msg=reply['changelog'])
        except TypeError:
            pass
        except KeyError:
            pass

    with ts3.query.TS3Connection("beta.theunlighted.com") as ts3miniconn:
        ts3miniconn.login(client_login_name='change', client_login_password='YyDJ4zvV')
        ts3miniconn.use(sid=1)
        ts3miniconn.keepalive()
        ts3miniconn.clientupdate(CLIENT_NICKNAME='Changelog v3')
        ts3miniconn.on_event.connect(change_notify)
        ts3miniconn.recv_in_thread()
        p1 = Process(target = rinsamaserv())
        p1.start()

# def my_event_handler(sender, event):
#         """
#         *sender* is the TS3Connection instance, that received the event.
#
#         *event* is a ts3.response.TS3Event instance, that contains the name
#         of the event and the data.
#         """
#         print("Event:")
#         print("  sender:", sender)
#         print("  event.event:", event.event)
#         print("  event.parsed:", event.parsed)
# Main
# ------------------------------------------------

USER = "serveradmin"
PASS = "mikhail9"

if __name__ == "__main__":
    # USER, PASS

    def rinsamaserv():
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 8040              # Arbitrary non-privileged port
        socksize = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print('Rin~Sama running on port: {}'.format(PORT))
        while True:
            print("Now listening...\n")
            conn, addr = s.accept()

            print('New connection from %s:%d' % (addr[0], addr[1]))
            data = conn.recv(socksize)
            if not data:
                conn.close()
            elif data == 'killsrv':
                conn.close()
                sys.exit()
            else:
                print(data)

    def centrigoserv(chann, data):
        client = Client("http://beta.theunlighted.com:8432/api/", "theunlighted", "3c88faac-7e6e-42ca-6d97-04ce1f969a25")
        params = {
            "channel": chann,
            "data": {
                "input": data
            }
        }
        client.add("publish", params)
        result, error = client.send()
    try:
        with ts3.query.TS3Connection("beta.theunlighted.com") as ts3conn:

            ts3conn.login(client_login_name=USER, client_login_password=PASS)
            ts3conn.use(sid=1)
            ts3conn.keepalive()

            me = ts3conn.whoami()[0]['client_id']
            ts3conn.clientupdate(CLIENT_NICKNAME='Rin~Sama v0.8.5')
            # Move the bot to the channel
            ts3conn.clientmove(cid=1620, clid=me)

            # Register notifs and handle in new thread
            ts3conn.servernotifyregister(event="server")
            ts3conn.servernotifyregister(event="textserver")
            ts3conn.servernotifyregister(event="textprivate")
            ts3conn.servernotifyregister(event="textchannel")
            ts3conn.servernotifyregister(event="channel", id_=4)
            # ts3conn.on_event.connect(my_event_handler)
            ts3conn.on_event.connect(Functions.welcomemsg)
            ts3conn.on_event.connect(Commands.commands)
            ts3conn.recv_in_thread()
            p4 = Process(target = changlog_instance())
            p4.start()
            print('Success')

    except Exception as e:
        print(e)
        sys.exit()

