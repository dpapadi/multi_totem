#!/bin/bash

cd '/home/ovx/OpenVirteX/utils/'

python ovxctl.py -n createNetwork tcp:localhost:8088 10.0.0.0 16
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:00:12
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:01:23
python ovxctl.py -n createSwitch 1 00:00:00:00:00:00:00:13
python ovxctl.py -n createPort 1 00:00:00:00:00:00:00:12 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:00:12 3 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:01:23 1 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:01:23 2 #(2)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:00:13 2 #(1)
python ovxctl.py -n createPort 1 00:00:00:00:00:00:00:13 3 #(2)
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:01 2 00:a4:23:05:00:00:00:02 1 spf 1
python ovxctl.py -n connectLink 1 00:a4:23:05:00:00:00:02 2 00:a4:23:05:00:00:00:03 2 spf 1
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:01 1 00:00:00:00:12:11
python ovxctl.py -n connectHost 1 00:a4:23:05:00:00:00:03 1 00:00:00:00:13:12
python ovxctl.py -n startNetwork 1

python ovxctl.py -n createNetwork tcp:localhost:8089 10.0.0.0 16
python ovxctl.py -n createSwitch 2 00:00:00:00:00:00:00:12
python ovxctl.py -n createSwitch 2 00:00:00:00:00:00:01:23
python ovxctl.py -n createSwitch 2 00:00:00:00:00:00:00:23
python ovxctl.py -n createPort 2 00:00:00:00:00:00:00:12 2 #(1)
python ovxctl.py -n createPort 2 00:00:00:00:00:00:00:12 3 #(2)
python ovxctl.py -n createPort 2 00:00:00:00:00:00:01:23 1 #(1)
python ovxctl.py -n createPort 2 00:00:00:00:00:00:01:23 3 #(2)
python ovxctl.py -n createPort 2 00:00:00:00:00:00:00:23 1 #(1)
python ovxctl.py -n createPort 2 00:00:00:00:00:00:00:23 2 #(2)
python ovxctl.py -n connectLink 2 00:a4:23:05:00:00:00:01 2 00:a4:23:05:00:00:00:02 1 spf 1
python ovxctl.py -n connectLink 2 00:a4:23:05:00:00:00:02 2 00:a4:23:05:00:00:00:03 2 spf 1
python ovxctl.py -n connectHost 2 00:a4:23:05:00:00:00:01 1 00:00:00:00:12:21
python ovxctl.py -n connectHost 2 00:a4:23:05:00:00:00:03 1 00:00:00:00:23:22
python ovxctl.py -n startNetwork 2

python ovxctl.py -n createNetwork tcp:localhost:8090 10.0.0.0 16
python ovxctl.py -n createSwitch 3 00:00:00:00:00:00:00:13
python ovxctl.py -n createSwitch 3 00:00:00:00:00:00:01:23
python ovxctl.py -n createSwitch 3 00:00:00:00:00:00:00:23
python ovxctl.py -n createSwitch 3 00:00:00:00:00:00:00:34
python ovxctl.py -n createPort 3 00:00:00:00:00:00:00:13 1 #(1)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:00:13 3 #(2)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:01:23 2 #(1)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:01:23 3 #(2)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:00:23 1 #(1)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:00:23 2 #(2)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:00:23 3 #(3)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:00:34 1 #(1)
python ovxctl.py -n createPort 3 00:00:00:00:00:00:00:34 4 #(2)
python ovxctl.py -n connectLink 3 00:a4:23:05:00:00:00:01 2 00:a4:23:05:00:00:00:02 1 spf 1
python ovxctl.py -n connectLink 3 00:a4:23:05:00:00:00:02 2 00:a4:23:05:00:00:00:03 2 spf 1
python ovxctl.py -n connectLink 3 00:a4:23:05:00:00:00:03 3 00:a4:23:05:00:00:00:04 2 spf 1
python ovxctl.py -n connectHost 3 00:a4:23:05:00:00:00:01 1 00:00:00:00:13:31
python ovxctl.py -n connectHost 3 00:a4:23:05:00:00:00:04 1 00:00:00:00:34:32
python ovxctl.py -n startNetwork 3

python ovxctl.py -n createNetwork tcp:localhost:8091 10.0.0.0 16
python ovxctl.py -n createSwitch 4 00:00:00:00:00:00:00:34
python ovxctl.py -n createPort 4 00:00:00:00:00:00:00:34 3 #(1)
python ovxctl.py -n createPort 4 00:00:00:00:00:00:00:34 2 #(2)
python ovxctl.py -n connectHost 4 00:a4:23:05:00:00:00:01 1 00:00:00:00:34:41
python ovxctl.py -n connectHost 4 00:a4:23:05:00:00:00:01 2 00:00:00:00:34:42
python ovxctl.py -n startNetwork 4