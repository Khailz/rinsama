import sys, os, time, random, ts3, sqlite3, threading, shlex, copy, \
    re, json, operator, requests, logging, paypalrestsdk, datetime, uuid, \
    pickle, socket, sched ,schedule, csv

def main():

    class Lottery:
        
        entries = {}
        winning_numbers =['{}'.format(random.randint(0,99)),
                          '{}'.format(random.randint(0,99)),
                          '{}'.format(random.randint(0,99)),
                          '{}'.format(random.randint(0,99)),
                          '{}'.format(random.randint(0,99)),
                          '{}'.format(random.randint(0,99))]
        winners = {}

        def __init__(self):
            self.users = []

        def checkusers(chkkey):

            try:

                url = 'http://beta.theunlighted.com/api/users'
                headers = {'Content-type': 'application/json'}

                r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                for key in r.json():

                    email = key['email']
                    points = key['points']
                    ts3id = key['ts3_identity']
                    username = key['username']
                    userid = key['id']
                    acckey = key['link_key']
                    groups = key['groups']

                    if ts3id == chkkey or acckey == chkkey:
                        return username, userid, email, ts3id, points, acckey, groups
            except TypeError as e:
                print(e)

        def getuserinfo(chkkey):

            try:

                url = 'http://beta.theunlighted.com/api/users'
                headers = {'Content-type': 'application/json'}

                r = requests.get(url, headers=headers, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                for key in r.json():

                    ts3id = key['ts3_identity']
                    points = key['points']

                    if ts3id == chkkey:
                        return points
            except TypeError as e:
                print(e)

        def minuspoints(chkkey, minuspoints):

            try:
                username, userid, email, ts3id, points, acckey, groups = Lottery.checkusers(chkkey=chkkey)
                url = 'http://beta.theunlighted.com/api/users/{}/'.format(userid)
                payload = {'points': points - minuspoints}
                r = requests.put(url, data=payload, auth=('{}'.format(settings.user), '{}'.format(settings.password)))
                print(r.status_code)
            except TypeError as e:
                print(e)

        def pickticket(self):
            number1 = random.randint(0, 99)
            number2 = random.randint(0, 99)
            number3 = random.randint(0, 99)
            number4 = random.randint(0, 99)
            number5 = random.randint(0, 99)
            number6 = random.randint(0, 99)
            self.lottery = [number1, number2, number3, number4, number5, number6]
            return self.lottery

        def userpicknumber(sender, event):
            notifytextmessage = event.event == 'notifytextmessage'
            if notifytextmessage:
                if event.parsed[0]["invokeruid"] == 'gaY4Wo/k0dCKvTYKcgWhgNmOUFU=':
                    return
                msg = event.parsed[0]['msg']
                clid = event.parsed[0]['invokerid']
                cliuid = event.parsed[0]['invokeruid']
                cliname = event.parsed[0]['invokername']
                username, userid, email, ts3id, points, acckey, groups = Lottery.checkusers(chkkey=cliuid)

                def getpick():
                    for x, y in Lottery.entries:
                        if cliuid == x:
                            return Lottery.entries[cliuid, False]


                def picktrue():
                    for x, y in Lottery.entries:
                        if cliuid == x:
                            Lottery.entries[cliuid, True] = Lottery.entries[cliuid, False]
                            del Lottery.entries[cliuid, False]
                            return Lottery.entries

                def pickfalse():
                    for x, y in Lottery.entries:
                        if cliuid == x:
                            Lottery.entries[cliuid, False] = Lottery.entries[cliuid, True]
                            del Lottery.entries[cliuid, True]
                            return Lottery.entries

                if msg.startswith('!'):
                    if cliuid == 'mjp3LhFUUS8ZM7zW8UV4tHTDyD4=':
                        if msg.startswith('!start'):
                            prize = msg[7:]
                            Lottery.massmsg(sender, event, prize)
                        if msg == '!winner':
                            winning_text = ""
                            if Lottery.choosewinner() == 1:
                                def parselist():
                                    print(Lottery.winners)
                                    print(Lottery.winning_numbers)
                                    for x, y in Lottery.winners.items():
                                        print(x)
                                        x = str(x).replace('=', '')
                                        print(x)
                                        for info in ts3conn.clientgetids(cluid='mjp3LhFUUS8ZM7zW8UV4tHTDyD4='):
                                            clid = info['clid']
                                            for info in ts3conn.clientinfo(clid=clid):
                                                return info['client_nickname'], y
                                try:
                                    name, numbermatch = parselist()
                                    if numbermatch == 1:
                                        c = '{}'.format(name) + ' matched {} numbers. 100 Points\n'.format(numbermatch)
                                        winning_text = winning_text + c
                                    if numbermatch == 2:
                                        c = '{}'.format(name) + ' matched {} numbers. 150 points + Main Prize!\n'.format(numbermatch)
                                        winning_text = winning_text + c
                                    if numbermatch == 3:
                                        c = '{}'.format(name) + ' matched {} numbers. 200 points + Main Prize!\n'.format(numbermatch)
                                        winning_text = winning_text + c
                                    if numbermatch == 4:
                                        c = '{}'.format(name) + ' matched {} numbers. 250 points + Main Prize!\n'.format(numbermatch)
                                        winning_text = winning_text + c
                                    if numbermatch == 5:
                                        c = '{}'.format(name) + ' matched {} numbers. 300 points + Main Prize!\n'.format(numbermatch)
                                        winning_text = winning_text + c
                                    if numbermatch == 6:
                                        c = '{}'.format(name) + ' matched {} numbers. 400 points + Main Prize!\n'.format(numbermatch)
                                        winning_text = winning_text + c
                                    for client in ts3conn.clientlist():
                                        if client['client_type'] == '1' or client['client_database_id'] == '1':
                                            continue
                                        else:
                                            ts3conn.sendtextmessage(targetmode=1,
                                                target=client['clid'],
                                                msg="The lottery has ended.\n [B][U]Results[/U][/B]\n{}".format(winning_text))
                                except KeyboardInterrupt as e:
                                    print(e)
                                    for client in ts3conn.clientlist():
                                        if client['client_type'] == '1' or client['client_database_id'] == '1':
                                            continue
                                        else:
                                            ts3conn.sendtextmessage(targetmode=1,
                                                    target=client['clid'],
                                                    msg="The lottery has ended. No Winners. The Winning Lotto was {}".format(Lottery.winning_numbers))

                    if msg == '!myticket':
                        try:
                            ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="Ticket {}".format(Lottery.entries[cliuid, False]))
                        except KeyError:
                            ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="You have no ticket")
                            return
                    if msg.startswith('!buyticket'):
                        numbers = msg[11:]
                        if msg == '':
                            ts3conn.sendtextmessage(targetmode=1,
                                            target=clid,
                                            msg="A valid Lotto should only contain numbers Ex. [color=blue]!buyticket 41 12 19 31 21 3[/color]")
                            return
                        if numbers:
                            ticket = numbers.split(' ')
                            newticket = [s for s in ticket if s.isdigit()]
                            Lottery.entries[cliuid, False] = newticket
                        try:
                            if len(Lottery.entries[cliuid, False]) <= 5 or len(Lottery.entries[cliuid, False]) >= 7:
                                ts3conn.sendtextmessage(targetmode=1,
                                                        target=clid,
                                                    msg="{} is not a valid Lotto. It should only contain numbers Ex. [color=blue]!buyticket 41 12 19 31 21 3[/color]".format(Lottery.entries[cliuid, False]))
                                Lottery.entries.pop(cliuid, False)
                                return
                        except KeyError:
                            ts3conn.sendtextmessage(targetmode=1,
                                                        target=clid,
                                                    msg="A valid Lotto should only contain numbers Ex. [color=blue]!buyticket 41 12 19 31 21 3[/color]")
                            Lottery.entries.pop(cliuid, False)
                            return


                        ts3conn.sendtextmessage(targetmode=1,
                                    target=clid,
                                     msg="\nThe Lotto you picked is {}\nThis ticket costs 100 points, are you sure you want to buy it? yes|no".format(Lottery.entries[cliuid, False]))

                        picktrue()
                try:
                    if Lottery.entries[cliuid, True]:
                        if msg == 'yes':
                            Lottery.minuspoints(chkkey=cliuid, minuspoints=100)
                            pickfalse()
                            ts3conn.sendtextmessage(targetmode=1,
                                                target=clid,
                                                msg="Ticket bought! Your ticket is {}. If you want to see your ticket again type !myticket".format(getpick()))
                            print('{} bought a ticket. {}'.format(cliuid, Lottery.entries[cliuid, True]))
                        if msg == 'no':
                            Lottery.minuspoints(chkkey=cliuid, minuspoints=100)
                            Lottery.entries.pop(cliuid, None)
                    if Lottery.entries[cliuid, False]:
                        ts3conn.sendtextmessage(targetmode=1,
                                                target=clid,
                                                msg="Ticket bought! Your ticket is {}. If you want to see your ticket again type !myticket".format(getpick()))
                except KeyError:
                    pass

        def choosewinner():
            for x, y in Lottery.entries.items():
                print('[] picked {}'.format(x, y))
                correctnums = [x for x in Lottery.winning_numbers if x in y]
                if len(correctnums) == 1:
                    Lottery.winners[x[0]] = 1
                if len(correctnums) == 2:
                    Lottery.winners[x[0]] = 2
                if len(correctnums) == 3:
                    Lottery.winners[x[0]] = 3
                if len(correctnums) == 4:
                    Lottery.winners[x[0]] = 4
                if len(correctnums) == 5:
                    Lottery.winners[x[0]] = 5
                if len(correctnums) == 6:
                    Lottery.winners[x[0]] = 6
            return 1

        def massmsg(sender, event, prize):
            for client in ts3conn.clientlist():
                if client['client_type'] == '1' or client['client_database_id'] == '1':
                    continue
                else:
                    ts3conn.clientpoke(msg="A Lottery has begun, Type !buyticket to start!",
                                                clid=client['clid'])
    class User(object):
        entries = {}
        def __init__(self, username):
            self.username = username
            self.status = False
            self.entries = {}
    try:
        with ts3.query.TS3Connection("beta.theunlighted.com") as ts3conn:
            date = ""
            ts3conn.login(client_login_name=USER, client_login_password=PASS)
            ts3conn.use(sid=1)
            ts3conn.keepalive()
            if date == "":
                date = datetime.datetime.now().strftime('%Y-%m-%d')
            me = ts3conn.whoami()[0]['client_id']
            ts3conn.clientupdate(CLIENT_NICKNAME='Lottery {}'.format(date))
            # Move the bot to the channel
            ts3conn.clientmove(cid=209, clid=me)

            # Register notifs and handle in new thread
            ts3conn.servernotifyregister(event="server")
            ts3conn.servernotifyregister(event="textserver")
            ts3conn.servernotifyregister(event="textprivate")
            ts3conn.servernotifyregister(event="textchannel")
            ts3conn.servernotifyregister(event="channel", id_=4)
            ts3conn.on_event.connect(Lottery.userpicknumber)
            ts3conn.recv_in_thread()
            while True:
                schedule.run_pending()
                time.sleep(1)

    except KeyboardInterrupt as e:
        print(e)
        sys.exit()

# Main
# ------------------------------------------------

USER = "notification"
PASS = "peJwutbF"

if __name__ == "__main__":
    # USER, PASS
    main()