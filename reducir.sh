#!/bin/bash
lines=$(which python3.6|wc -l)
if [ $lines -eq 1 ];
then
    cd Reductor/
    python3.6 main.py
else
    apt-get install software-properties-common -y
    add-apt-repository ppa:jonathonf/python-3.6
    apt-get update -y
    apt-get install python3.6 -y
    cd Reductor/
    python3.6 main.py
fi

