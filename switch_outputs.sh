#!/bin/bash

# --- CONFIGURATION ---
VIRTUAL_SINK_NAME="Simultaneous Output"
SPEAKER_FULL_NODE="alsa_output.pci-0000_12_00.6.analog-stereo"
LINE_IN_NODE="alsa_input.pci-0000_12_00.6.analog-stereo"

# --- STATE DATABASE ---
declare -A VOLUME_DB
VOLUME_DB["$SPEAKER_FULL_NODE"]="0.50"
ACTIVE_LINKS=""
LAST_STATE="none"
MISSING_COUNT=0

get_node_id() {
    wpctl status -n | grep "$1" | head -n1 | sed -E 's/[^0-9]*([0-9]+).*/\1/'
}

get_volume() {
    wpctl get-volume "$1" | awk '{print $2}'
}

send_note() {
    notify-send -t 3000 -i "$2" "Audio Manager" "$1"
}

echo "--- Starting Hardened Audio Manager V6 ---"

# 1. Create Virtual Sink hub
if ! wpctl status | grep -q "$VIRTUAL_SINK_NAME"; then
    pw-cli create-node adapter '{ factory.name=support.null-audio-sink node.name="'"$VIRTUAL_SINK_NAME"'" node.description="'"$VIRTUAL_SINK_NAME"'" media.class=Audio/Sink object.linger=true audio.position=[FL FR] }'
    sleep 2
fi

# 2. Setup Default Hub
VIRT_ID=$(get_node_id "$VIRTUAL_SINK_NAME")
[[ -n "$VIRT_ID" ]] && wpctl set-default "$VIRT_ID" && wpctl set-mute "$VIRT_ID" 0

while true; do
    # 3. Detect Bluetooth (Targeting the 'internal' naming convention for stability)
    BT_NODES=$(pw-link -o | grep "bluez_output_internal" | cut -d':' -f1 | sort -u)
    SPEAKER_ID=$(get_node_id "$SPEAKER_FULL_NODE")
    
    # --- LINE-IN LINKING ---
    if [[ -z "$LINE_IN_LINKED" ]] && wpctl status -n | grep -q "$LINE_IN_NODE"; then
        pw-link "$LINE_IN_NODE:capture_FL" "$VIRTUAL_SINK_NAME:playback_FL" 2>/dev/null
        pw-link "$LINE_IN_NODE:capture_FR" "$VIRTUAL_SINK_NAME:playback_FR" 2>/dev/null
        LINE_IN_LINKED="yes"
    fi

    # --- BLUETOOTH LOGIC ---
    if [[ -n "$BT_NODES" ]]; then
        MISSING_COUNT=0 
        
        if [[ "$LAST_STATE" != "headset" ]]; then
            # Save Speaker Volume and Mute
            if [[ -n "$SPEAKER_ID" ]]; then
                VOLUME_DB["$SPEAKER_FULL_NODE"]=$(get_volume "$SPEAKER_ID")
                wpctl set-mute "$SPEAKER_ID" 1
            fi
            LAST_STATE="headset"
        fi

        for NODE in $BT_NODES; do
            if [[ ! "$ACTIVE_LINKS" =~ "$NODE" ]]; then
                echo "Attempting link for: $NODE"
                
                # Link Sink Monitor -> Headset Playback
                pw-link "$VIRTUAL_SINK_NAME:monitor_FL" "$NODE:playback_FL" 2>/dev/null
                pw-link "$VIRTUAL_SINK_NAME:monitor_FR" "$NODE:playback_FR" 2>/dev/null
                
                # Restore Volume for this specific headset
                CID=$(get_node_id "$NODE")
                SAVED_VOL=${VOLUME_DB["$NODE"]:-0.40}
                if [[ -n "$CID" ]]; then
                    wpctl set-mute "$CID" 0
                    wpctl set-volume "$CID" "$SAVED_VOL"
                fi
                
                ACTIVE_LINKS="$ACTIVE_LINKS $NODE"
                send_note "Headset Linked: $NODE" "audio-headphones"
            fi
        done
    else
        # --- DISCONNECTION GRACE PERIOD ---
        if [[ "$LAST_STATE" == "headset" ]]; then
            ((MISSING_COUNT++))
            if [[ $MISSING_COUNT -gt 3 ]]; then
                ACTIVE_LINKS=""
                if [[ -n "$SPEAKER_ID" ]]; then
                    RESTORE_VOL=${VOLUME_DB["$SPEAKER_FULL_NODE"]}
                    wpctl set-mute "$SPEAKER_ID" 0
                    wpctl set-volume "$SPEAKER_ID" "$RESTORE_VOL"
                    send_note "Headsets Disconnected\nSpeakers Restored" "audio-speakers"
                fi
                LAST_STATE="none"
            fi
        fi
    fi

    # Cleanup removed headsets from tracker
    for LINKED in $ACTIVE_LINKS; do
        if ! echo "$BT_NODES" | grep -q "$LINKED"; then
            ACTIVE_LINKS=$(echo "$ACTIVE_LINKS" | sed "s/$LINKED//")
        fi
    done

    sleep 1
done