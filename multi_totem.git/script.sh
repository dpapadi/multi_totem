#!/bin/bash

cd ~/kafka
sh bin/zookeeper-server-start.sh config/zookeeper.properties
sh bin/kafka-server-start.sh config/server.properties