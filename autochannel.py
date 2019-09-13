#!/usr/bin/python
import sys, os, time, random, ts3, sqlite3, threading, shlex, copy, \
    re, json, operator, requests, logging, paypalrestsdk, datetime, uuid, \
    pickle, socket, sched, schedule, csv


def main():
    class ChannelRanker:

        def rankchannel():
            data = {}
            for channel in ts3conn.channellist():
                if channel['pid'] != '28':
                    continue
                data[channel['cid']] = channel['total_clients']
                with open(os.path.join(BASE_DIR, 'Functions/data/channelrank.json'), 'w') as outfile:
                    json.dump(data, outfile)

            # for info in ts3conn.channelinfo(cid=209):
            #     print(info)

        # def ranks(self):
        #     self.channels = []
        #     self.

    class AFKChannelDeleter:


        def deletechans():
            print('Searching for unused channels')
            for channel in ts3conn.channellist(secondsempty=True):
                exemptlist =['17', '18', '2076', '144', '439', '1076', '29', '5', '4', '209',
                             '1620', '1227', '1714', '64', '3', '42', '1', '1568', '61', '62',
                             '1034', '40', '724', '255', '6', '30', '31', '32', '33', '580', '27',
                             '1167', '69', '34', '68', '343', '616', '2185', '41', '1187', '257', '583',
                             '874', '875', '838', '141', '50', '441', '719', '1079', '1296', '1363', '1364',
                             '1522', '1523', '1597', '1685', '1435', '28', '2', '45']

                # ss.append(str(channel['cid']))
                if str(channel['cid']) in exemptlist:
                        continue
                if int(channel['seconds_empty']) > 1209600:
                    if str(channel['cid']) in exemptlist:
                        continue
                    ts3conn.channeldelete(cid=channel['cid'], force=True)
            print('Search for unused channels done')

    try:
        with ts3.query.TS3Connection("{}".format(settings.ts_url)) as ts3conn:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ts3conn.login(client_login_name=USER, client_login_password=PASS)
            ts3conn.use(sid=1)
          

            me = ts3conn.whoami()[0]['client_id']
            ts3conn.clientupdate(CLIENT_NICKNAME='Deleting Unused channels')
            # Move the bot to the channel
            ts3conn.clientmove(cid=209, clid=me)

        
            print("Looking out for unused channels")
            ChannelRanker.rankchannel()
            schedule.every().minute.do(AFKChannelDeleter.deletechans)
            while True:
                schedule.run_pending()
                time.sleep(1)

    except KeyboardInterrupt as e:
        print(e)
        sys.exit()


# Main
# ------------------------------------------------

USER = "serveradmin"
PASS = "{}".format(settings.password)

if __name__ == "__main__":
    # USER, PASS
    main()
