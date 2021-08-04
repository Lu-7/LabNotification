#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import nfc
import time
import csv
import json
import requests

class Notify:
    def __init__(self):
        self.memlist = []
        self.service_code = 0x200B #service code
        self.clf = nfc.ContactlessFrontend('usb')
        self.read_mem_list()
        self.run()

    def on_connect_nfc(self, tag):
        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            try:
                sc = nfc.tag.tt3.ServiceCode(self.service_code >> 6, self.service_code & 0x3f)
                bc = nfc.tag.tt3.BlockCode(0,service=0)
                data = tag.read_without_encryption([sc],[bc])
                sid =  str(data[0:8].decode("utf-8"))
                #print("Tokai:" + sid) //debug print
                for i in range(len(self.memlist)):
                    if sid == self.memlist[i][0]:
                        if(self.memlist[i][2]=="0"):
                            print("{} 入室".format(self.memlist[i][1]))
                            self.ifttt_post(str(self.memlist[i][1]), "入室")
                            self.memlist[i][2]="1"
                        else:
                            print("{} 退室".format(self.memlist[i][1]))
                            self.ifttt_post(str(self.memlist[i][1]), "退室")
                            self.memlist[i][2]="0"
            except Exception as e:
                print("error: %s" % e)
        else:
            print("error: tag isn't Type3Tag")

    def read_mem_list(self):
        print("-start read member data-")
        with open("member_list.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                self.memlist.append(row)
                print(row)
            print("end")

    def ifttt_post(self, val1, val2):
        url = "https://maker.ifttt.com/trigger/<event_name>/json/with/key/<your_key>"

        headers = {
            'Content-Type': 'application/json',
        }

        data = '{"value1":"%s","value2":"%s"}' % (val1, val2)
        
        res = requests.post(url, headers=headers, data=data.encode('utf-8'))
        print(res.text)

    def run(self):
        while True:
            self.clf.connect(rdwr={'on-connect': self.on_connect_nfc})
            time.sleep(5)
  
if __name__ == "__main__":
    Notify()
