#!/bin/sh

# Will grab the running window and record it


INFO=$(xwininfo -frame)

WIN_GEO=$(echo $INFO | grep -oEe 'geometry [0-9]+x[0-9]+' |\
    grep -oEe '[0-9]+x[0-9]+')
WIN_XY=$(echo $INFO | grep -oEe 'Corners:\s+\+[0-9]+\+[0-9]+' |\
    grep -oEe '[0-9]+\+[0-9]+' | sed -e 's/+/,/' )

ffmpeg -f x11grab -y -r 15 -s $WIN_GEO -i :0.0+$WIN_XY -vcodec mpeg4 -an -sameq -threads 2 $1.avi
