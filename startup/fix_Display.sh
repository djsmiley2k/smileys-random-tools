#!/bin/bash
############
# Fixes displayPort losing resolution settings for X
############

sleep 4

xrandr --output DisplayPort-0 --off --output DVI-1 --off --output DVI-0 --mode 1920x1080 --pos 0x0 --rotate normal --output HDMI-0 --mode 1920x1080 --pos 1920x0 --rotate normal

