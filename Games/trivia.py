import sys, ts3, random

def triviarin():



    with ts3.query.TS3Connection("beta.theunlighted.com") as ts3conn:
        ts3conn.login(client_login_name=USER, client_login_password=PASS)
        ts3conn.use(sid=1)
        ts3conn.keepalive()

        me = ts3conn.whoami()[0]['client_id']
        ts3conn.clientupdate(CLIENT_NICKNAME='Rin~Sama Trivia #{}'.format(random.randint(0, 10)))
        # Move the bot to the channel
        ts3conn.clientmove(cid=int('{}'.format(sys.argv[1])), clid=me)

        # Register notifs and handle in new thread
        ts3conn.servernotifyregister(event="server")
        ts3conn.servernotifyregister(event="textserver")
        ts3conn.servernotifyregister(event="textprivate")
        ts3conn.servernotifyregister(event="textchannel")
        ts3conn.servernotifyregister(event="channel", id_=4)
        ts3conn.sendtextmessage(targetmode=2, target=sys.argv[1], msg="Test" )
        ts3conn.recv_in_thread()
        input("> Hit enter to finish.\n")