#!/bin/bash
ID=$(wpctl status -n | grep "alsa_input.pci-0000_12_00.6.analog-stereo" | head -n1 | sed -E 's/[^0-9]*([0-9]+).*/\1/')

if [[ -n "$ID" ]]; then
    wpctl set-volume "$ID" 5%-
    VOL=$(wpctl get-volume "$ID" | awk '{print $2 * 100 "%"}')
    notify-send -t 1000 -i "audio-input-microphone" "Line-In Volume" "Level: $VOL"
else
    notify-send -t 2000 -i "dialog-error" "Line-In Volume" "Device not found!"
fi
