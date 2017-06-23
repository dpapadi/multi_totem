#!/bin/bash

if [ $# -lt 2 ]
then
    echo "$0 needs more arguments. (normal, 2bsw, bsw, vlink, all) controller_port1 etc"
    exit
fi

case "$1" in

    normal) if [ $# -ne 2 ]
            then
                echo "wrong number of inputs!!!!"
                exit
            fi
            echo "normal: $@"
            exit
            ;;
    2bsw)   if [ $# -ne 2 ]
            then
                echo "wrong number of inputs!!!!"
                exit
            fi
            echo "2bsw: $@"
            exit
            ;;
    bsw)    if [ $# -ne 2 ]
            then
                echo "wrong number of inputs!!!!"
                exit
            fi
            echo "bsw: $@"
            exit
            ;;
    vlink)  if [ $# -ne 2 ]
            then
                echo "wrong number of inputs!!!!"
                exit
            fi
            echo "vlink: $@"
            exit
            ;;
    all)    if [ $# -ne 2 ]
            then
                echo "wrong number of inputs!!!!"
                exit
            fi
            echo "all: $@"
            exit
            ;;
    *)      echo "wrong first attribute"
            exit
            ;;
esac