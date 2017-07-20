#!/bin/bash

cd '/home/ovx/OpenVirteX/utils/'

python ovxctl.py -n createNetwork tcp:localhost:8088 10.0.0.0 16
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:11:01
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:22:02
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:33:03
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:44:04
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:55:05

python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 5 #(5)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 3 #(3)



python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:01 3 00:a4:23:05:00:00:00:02 2 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:03 3 00:a4:23:05:00:00:00:02 3 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:04 3 00:a4:23:05:00:00:00:02 4 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:05 3 00:a4:23:05:00:00:00:02 5 spf 1

python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:01 1 00:00:00:00:01:11
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:01 2 00:00:00:00:01:12
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 2 00:00:00:00:03:31
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 1 00:00:00:00:03:32
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 2 00:00:00:00:04:41
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 1 00:00:00:00:04:42
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:05 2 00:00:00:00:05:51
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:05 1 00:00:00:00:05:52



python ovxctl.py -n startNetwork 1