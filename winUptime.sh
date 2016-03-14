#!/bin/bash

# Shamelessly borrowed from http://correctlife.blogspot.de/2011/02/wrapper-on-checkntuptime.html

HOSTADDRESS=$1
MAXWARN=$2 # in hours
MAXCRIT=$3 # in hours

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

SECONDS=`/usr/local/nagios/libexec/check_nt -H $HOSTADDRESS -p 12489 -s $ekR3t $2 $3`
#### IS:           6817
#### SHOULD BE:    WARNING: uptime: 1:53 < warning|'uptime'=6817000;172800000;3600000;

HOURS=$(( $SECONDS / 60 / 60 ))
SECONDSINHOURS=$(( $HOURS * 60 * 60 ))
DAYS=$(( $HOURS / 24 ))
REMAININGSECONDS=$(( $SECONDS - $SECONDSINHOURS ))
MINUTES=$(( $REMAININGSECONDS / 60 ))
FORMEDUPTIME="${DAYS}"

if [[ $DAYS -ge $MAXCRIT ]]; then
    echo "CRITICAL: System up over ${MAXCRIT} days."
    exit 2
fi

if [[ $DAYS -ge $MAXWARN ]]; then
    echo "WARNING: System up over ${MAXWARN} days."
    exit 1
fi

echo "OK. Uptime $FORMEDUPTIME Days."
exit 0
