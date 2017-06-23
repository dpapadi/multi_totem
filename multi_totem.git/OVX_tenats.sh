#!/bin/bash

if [[ $1 -eq "normal" or $1 -eq "2bsw" or $1 -eq "bsw" or $1 -eq "vlink" and $# -ne 2 ]]
then
    echo "Provide 2 arguments (normal, 2bsw, bsw, vlink) port"
    echo "You provided $# arguments"
    exit
fi

if [[ $1 -eq "all" and $# -ne 5 ]]
then
    echo "Provide 5 arguments (normal, 2bsw, bsw, vlink) port"
    echo "You provided $# arguments"
    exit
fi

case "$1" in

    normal) if [ $# -ne 2 ]
            then
                echo "wrong number of arguments!!!! n --> $#"
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
    all)    if [ $# -ne 5 ]
            then
                echo "wrong number of inputs!!!!"
                exit
            fi
            echo "all: $@"
            exit
            ;;
    *)      echo "wrong first attribute. (normal, 2bsw, bsw, vlink, all)"
            exit
            ;;
esac