#!/bin/bash

if [ $# -lt 2 ]
then
    echo "$0 needs more arguments. (normal, 2bsw, bsw, vlink, all) controller_port1 etc"
fi

case "1" in

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
    *)      echo "wrong first attribute"
            exit
            ;;
esac