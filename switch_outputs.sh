#!/bin/bash

# --- CONFIGURATION ---
VIRTUAL_SINK_NAME="Simultaneous Output"
SPEAKER_FULL_NODE="alsa_output.pci-0000_12_00.6.analog-stereo"
LINE_IN_NODE="alsa_input.pci-0000_12_00.6.analog-stereo"

# --- VOLUME DATABASE ---
declare -A VOLUME_DB
VOLUME_DB["$SPEAKER_FULL_NODE"]="0.50" # Default startup volume

get_node_id() {
    wpctl status -n | grep "$1" | head -n1 | sed -E 's/[^0-9]*([0-9]+).*/\1/'
}

get_volume() {
    wpctl get-volume "$1" | awk '{print $2}'
}

# Helper for desktop notifications
send_note() {
    # Uses a 'audio-headset' or 'audio-speakers' icon if available
    notify-send -i "$2" "Audio Manager" "$1"
}

echo "--- Starting Smart Audio Manager ---"

# 1. Create Virtual Sink hub
if ! wpctl status | grep -q "$VIRTUAL_SINK_NAME"; then
    pw-cli create-node adapter '{ factory.name=support.null-audio-sink node.name="'"$VIRTUAL_SINK_NAME"'" node.description="'"$VIRTUAL_SINK_NAME"'" media.class=Audio/Sink object.linger=true audio.position=[FL FR] }'
    sleep 2
fi

# 2. Setup Default Hub
VIRT_ID=$(get_node_id "$VIRTUAL_SINK_NAME")
[[ -n "$VIRT_ID" ]] && wpctl set-default "$VIRT_ID" && wpctl set-mute "$VIRT_ID" 0

echo "Monitoring... (Press Ctrl+C to stop)"

LAST_STATE="none"
ALREADY_LINKED_BT=""

while true; do
    BT_NODES=$(pw-link -l | grep "bluez_output" | cut -d':' -f1 | sort -u)
    SPEAKER_ID=$(get_node_id "$SPEAKER_FULL_NODE")
    
    # --- DYNAMIC LINE-IN LINKING ---
    if [[ -z "$LINE_IN_LINKED" ]] && wpctl status -n | grep -q "$LINE_IN_NODE"; then
        pw-link "$LINE_IN_NODE:capture_FL" "$VIRTUAL_SINK_NAME:playback_FL" 2>/dev/null
        pw-link "$LINE_IN_NODE:capture_FR" "$VIRTUAL_SINK_NAME:playback_FR" 2>/dev/null
        LINE_IN_ID=$(get_node_id "$LINE_IN_NODE")
        [[ -n "$LINE_IN_ID" ]] && wpctl set-mute "$LINE_IN_ID" 0
        send_note "External Device Detected & Linked" "audio-input-microphone"
        LINE_IN_LINKED="yes"
    fi

    # --- BLUETOOTH LOGIC ---
    if [[ -n "$BT_NODES" ]]; then
        if [[ "$LAST_STATE" != "headset" ]]; then
            # Save Speaker Volume
            if [[ -n "$SPEAKER_ID" ]]; then
                VOLUME_DB["$SPEAKER_FULL_NODE"]=$(get_volume "$SPEAKER_ID")
                wpctl set-mute "$SPEAKER_ID" 1
            fi
            LAST_STATE="headset"
        fi

        for NODE in $BT_NODES; do
            CURRENT_BT_ID=$(get_node_id "$NODE")
            if [[ ! "$ALREADY_LINKED_BT" =~ "$NODE" ]]; then
                pw-link "$VIRTUAL_SINK_NAME:monitor_FL" "$NODE:playback_FL" 2>/dev/null
                pw-link "$VIRTUAL_SINK_NAME:monitor_FR" "$NODE:playback_FR" 2>/dev/null
                
                # Restore Volume
                SAVED_VOL=${VOLUME_DB["$NODE"]:-0.40}
                [[ -n "$CURRENT_BT_ID" ]] && wpctl set-mute "$CURRENT_BT_ID" 0 && wpctl set-volume "$CURRENT_BT_ID" "$SAVED_VOL"
                
                # NOTIFICATION
                send_note "Routing audio to Headset\nVolume restored to $(echo "$SAVED_VOL * 100" | bc | cut -d. -f1)%" "audio-headphones"
                
                ALREADY_LINKED_BT="$ALREADY_LINKED_BT $NODE"
            fi
        done
    else
        # SPEAKER MODE
        if [[ "$LAST_STATE" == "headset" ]]; then
            # Save Headset Volumes
            for NODE in $ALREADY_LINKED_BT; do
                HID=$(get_node_id "$NODE")
                if [[ -n "$HID" ]]; then
                    VOLUME_DB["$NODE"]=$(get_volume "$HID")
                fi
            done
            
            # Restore Speaker Volume
            if [[ -n "$SPEAKER_ID" ]]; then
                RESTORE_VOL=${VOLUME_DB["$SPEAKER_FULL_NODE"]}
                wpctl set-mute "$SPEAKER_ID" 0
                wpctl set-volume "$SPEAKER_ID" "$RESTORE_VOL"
                
                # NOTIFICATION
                send_note "Headset disconnected\nRestoring Speakers ($(echo "$RESTORE_VOL * 100" | bc | cut -d. -f1)%)" "audio-speakers"
            fi
            
            LAST_STATE="none"
            ALREADY_LINKED_BT=""
        fi
    fi

    sleep 0.5
done
