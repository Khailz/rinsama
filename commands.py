from main import *

class Command:
    def myprofile(sender, event):
        msg = event.parsed[0]['msg']
        clid = event.parsed[0]['invokerid']
        cliuid = event.parsed[0]['invokeruid']
        userinfo = Functions.checkusers(cliuid=cliuid)
        ts3conn.sendtextmessage(targetmode=1, target=clid, msg="Please wait while I fetch your info....")
        try:
            if userinfo:
                username, userid, email, ts3id, points, rpgrace = Functions.checkusers(cliuid=cliuid)
                ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg=reply['clistats'].format(username, email, ts3id, points, rpgrace)
                                        )
            if userinfo is None:
                ts3conn.sendtextmessage(targetmode=1,
                                        target=clid,
                                        msg="You are not registered."
                                        )
        except TypeError as e:
            print(e)
