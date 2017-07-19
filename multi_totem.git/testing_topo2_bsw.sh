#!/bin/bash

cd '/home/ovx/OpenVirteX/utils/'

python ovxctl.py -n createNetwork tcp:localhost:8088 10.0.0.0 16
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:11:01,00:00:00:00:00:00:22:02,00:00:00:00:00:00:33:03,00:00:00:00:00:00:44:04 #big switch (s1, s2, s3, s4)
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:55:05 #left
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:66:06 #right
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:77:07 #top
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:88:08 #bottom

python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 2 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 2 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:77:07 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:77:07 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:77:07 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 3 #(3)

python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:01 1 00:a4:23:05:00:00:00:02 3 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:01 2 00:a4:23:05:00:00:00:04 3 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:01 3 00:a4:23:05:00:00:00:03 3 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:01 4 00:a4:23:05:00:00:00:05 3 spf 1

python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:02 2 00:00:00:00:05:51
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:02 1 00:00:00:00:05:52
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 1 00:00:00:00:06:61
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 2 00:00:00:00:06:62
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 2 00:00:00:00:07:71
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 1 00:00:00:00:07:72
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:05 1 00:00:00:00:08:81
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:05 2 00:00:00:00:08:82

python ovxctl.py -n startNetwork 1

