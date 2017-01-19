#!/bin/bash

cd ~/kafka/kafka_2.11-0.10.1.0
sh bin/zookeeper-server-start.sh config/zookeeper.properties &
sh bin/kafka-server-start.sh config/server.properties &&