#!/bin/bash

cd /home/tim/1000photos
rm /home/tim/1000photos/*

IFS=$'\n'; for f in $(find /backups/googlePhotos/photos/ -type f -name '*.jpg' | shuf -n1000); do cp $f .; done

for img in *.jpg; do

   convert                   \
      "${img}"               \
     -fill black             \
     -undercolor white       \
     -pointsize 14           \
     -gravity south          \
     -annotate +0+5 "${img}" \
      "${img}"

done
