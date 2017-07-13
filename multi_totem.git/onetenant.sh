#!/bin/bash

cd '/home/ovx/OpenVirteX/utils/'

python ovxctl.py -n createNetwork tcp:localhost:8088 10.0.0.0 16
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:11:01
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:22:02
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:33:03
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:44:04
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:55:05 #int1
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:66:06 #int2
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:77:07 #int3
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:88:08 #gtw

python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:11:01 5 #(5)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:22:02 5 #(5)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:33:03 5 #(5)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:44:04 5 #(5)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:88:08 5 #(5)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:55:05 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 3 #(3)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 4 #(4)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:66:06 5 #(5)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:77:07 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:77:07 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:77:07 3 #(3)

python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:01 5 00:a4:23:05:00:00:00:05 2 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:03 5 00:a4:23:05:00:00:00:05 4 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:06 2 00:a4:23:05:00:00:00:05 3 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:06 3 00:a4:23:05:00:00:00:02 5 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:06 5 00:a4:23:05:00:00:00:08 5 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:06 4 00:a4:23:05:00:00:00:07 2 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:04 5 00:a4:23:05:00:00:00:07 3 spf 1

python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:01 1 00:00:00:00:01:11
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:01 2 00:00:00:00:01:12
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:01 3 00:00:00:00:01:13
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:01 4 00:00:00:00:01:14
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:02 2 00:00:00:00:02:21
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:02 4 00:00:00:00:02:22
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:02 3 00:00:00:00:02:23
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:02 1 00:00:00:00:02:24
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 4 00:00:00:00:03:31
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 1 00:00:00:00:03:32
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 2 00:00:00:00:03:33
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 3 00:00:00:00:03:34
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 4 00:00:00:00:04:41
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 3 00:00:00:00:04:42
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 2 00:00:00:00:04:43
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:04 1 00:00:00:00:04:44
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:08 4 00:00:00:00:08:81
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:08 2 00:00:00:00:08:82
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:08 1 00:00:00:00:08:83
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:08 3 00:00:00:00:08:84
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:05 1 00:00:00:00:01:51
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:06 1 00:00:00:00:06:61
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:07 1 00:00:00:00:07:71

python ovxctl.py -n startNetwork 1