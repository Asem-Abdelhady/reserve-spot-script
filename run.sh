#!/bin/bash
cd /home/asem/PycharmProjects/reserve-spot
source ./venv/bin/activate
echo 'Entered the cronjob1' >./cronjob.txt
python3 ./main.py $1 $2 &>./out.log
echo 'Exited the cronjob1' >./cronjob_exit.txt
