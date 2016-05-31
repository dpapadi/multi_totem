#!/bin/bash

sudo ovs-vsctl -- --id=@sflow1 create sflow agent=s1 target=\"localhost:6343\" header=128 sampling=10 polling=3600 -- set bridge s1 sflow=@sflow1
