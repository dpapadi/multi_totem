#!/bin/bash

cd ~/kafka
sh bin/zookeeper-server-start config/zookeeper.properties
sh bin/kafka-server-start config/server.properties