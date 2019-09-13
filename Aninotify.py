#!/usr/bin/python
import sys, os, time, random, ts3, sqlite3, threading, shlex, copy, \
    re, json, operator, requests, logging, paypalrestsdk, datetime, uuid, \
    pickle, socket, sched, schedule, csv


def main():
    class AnimeNotifier:

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
            params = {'access_token': '{}'.format(AnimeNotifier.gettoken())}
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
                                AnimeNotifier.check_anime_times(ts3uid=key["ts3_identity"])
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
                print('Error FUCKING ERROR')
            listtext = ""
            clisettings = AnimeNotifier.getusersettings(chkkey=ts3uid)
            for anime, title in clisettings['notify'].items():
                try:
                    title, a = AnimeNotifier.checkrelease(search=anime)
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
                print('Fucking another ERROR')
    try:
        with ts3.query.TS3Connection("{}".format(settings.ts_url)) as ts3conn:

            ts3conn.login(client_login_name=USER, client_login_password=PASS)
            ts3conn.use(sid=1)
            

            me = ts3conn.whoami()[0]['client_id']
            # Move the bot to the channel
            ts3conn.clientmove(cid=209, clid=me)

            # Register notifs and handle in new thread
            
            print("Aninotify Started")
            AnimeNotifier.checkusers()
            schedule.every().hour.do(AnimeNotifier.checkusers)
            while True:
                schedule.run_pending()
                time.sleep(1)

    except Exception as e:
        print(e)
        sys.exit()


# Main
# ------------------------------------------------

USER = "serveradmin"
PASS = "{}".format(settings.password)

if __name__ == "__main__":
    # USER, PASS
    main()
