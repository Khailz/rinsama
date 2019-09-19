import sys, os, random, threading, json, logging, uuid, pickle, socket, ts3, requests
from threading import Thread
from Functions import Aninotify, Leaderboard, Rinserver, rin, autochannel, sayings

if __name__ == "__main__":
    p = Thread(target=Aninotify.main)
    p1 = Thread(target=Rinserver.main)
    p2 = Thread(target=Leaderboard.main)
    p3 = Thread(target=autochannel.main)
    p4 = Thread(target=rin.main)
    p.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
