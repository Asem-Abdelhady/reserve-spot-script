#!/bin/bash
cd /home/asem/PycharmProjects/reserve-spot
source ./venv/bin/activate
echo 'Entered the cronjob1' >./cronjob_entry.txt
#python3 ./main.py $1 $2 &>./out.log
#echo 'Finished main' >./cronjob_exit.txt
python3 ./main2.py $1 $2 &>./out.log
echo 'Finished main2' >./cronjob_exit2.txt
