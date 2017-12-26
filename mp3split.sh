#!/bin/bash
big="$1"
duration_stamp=$(ffmpeg -i "$big" 2>&1 | grep Duration | sed 's/^.*Duration: *\([^ ,]*\),.*/\1/g')
title=$(ffmpeg -i "$big" 2>&1  | grep "title *:" | sed 's/^.*title *: *\(.*\)/\1/g')
# get minutes as a raw integer number (rounded up)
prefix=$(basename "$big" .mp3)
echo $duration_stamp
mins=$(echo "$duration_stamp" | sed 's/\([0-9]*\):\([0-9]*\):\([0-9]*\)\.\([0-9]*\)/\1*60+\2+\3\/60+\4\/60\/100/g' | bc -l | python -c "import math; print int(math.ceil(float(raw_input())))")
ss="0"
count="1"
total_count=$(echo "$mins/3+1" | bc)
while [ "$ss" -lt "$mins" ]
do
  zcount=$(printf "%05d" $count)
  ss_hours=$(echo "$ss/60" | bc)
  ss_mins=$(echo "$ss%60" | bc)
  ss_stamp=$(printf "%02d:%02d:00" $ss_hours $ss_mins)
  ffmpeg -i "$big" -acodec copy -t 00:03:00 -ss $ss_stamp -metadata track="$count/$total_count" -metadata title="$title $zcount" "$prefix-$zcount.mp3" 
  ss=$[$ss+3]
  count=$[$count+1]
done
