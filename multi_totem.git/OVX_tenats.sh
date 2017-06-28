#!/bin/bash

echo << EOF
function normal {
    cd '/home/ovx/OpenVirteX/utils/'
    python ovxctl.py -n createNetwork tcp:localhost:"$1" 10.0.0.0 16
    python ovxctl.py -n createSwitch "$2" 00:00:00:00:00:00:02:00
    python ovxctl.py -n createSwitch "$2" 00:00:00:00:00:00:03:00
    python ovxctl.py -n createSwitch "$2" 00:00:00:00:00:00:04:00
    python ovxctl.py -n createSwitch "$2" 00:00:00:00:00:00:05:00
    python ovxctl.py -n createPort "$2" 00:00:00:00:00:00:00:2:00 1
    }
EOF

if [ $# -lt 1 ]
then
    echo "Provide arguments: (normal, 2bsw, bsw, vlink, all) port1 (port2 port3 port4)"
    exit
fi

if [ $1 == "normal" ] || [ $1 == "2bsw" ] || [ $1 == "bsw" ] || [ $1 == "vlink" ]
then
    if [ $# -ne 2 ]
    then
        echo "Provide 2 arguments: (normal, 2bsw, bsw, vlink) port"
        echo "You provided $# arguments"
        exit
    fi
fi

if [[ $1 == "all" && "$#" -ne 5 ]]
then
    echo "Provide 5 arguments: all port1 port2 port3 port4"
    echo "You provided $# arguments"
    exit
fi

case "$1" in

    normal) echo "normal: $@"
            exit
            ;;
    2bsw)   echo "2bsw: $@"
            exit
            ;;
    bsw)    echo "bsw: $@"
            exit
            ;;
    vlink)  echo "vlink: $@"
            exit
            ;;
    all)    echo "all: $@"
            exit
            ;;
    *)      echo "wrong first attribute. (normal, 2bsw, bsw, vlink, all)"
            exit
            ;;
esac