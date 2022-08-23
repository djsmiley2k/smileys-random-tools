#!/bin/bash

cd /home/tim/bin/scripts

echo "## Starting Backups ##" > /backups/backup.log
date >> /backups/backup.log

start=`date +%s`

for x in ./backupM*; do time $x; done >> /backups/backup.log 2>&1

for x in ./backupS*; do time $x; done >> /backups/backup.log 2>&1

date >> /backups/backup.log

echo "Duration: $((($(date +%s)-$start)/60)) minutes" >> /backups/backup.log
