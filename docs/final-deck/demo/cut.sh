#!/bin/bash
# Cut the 6 Nov demo recording to ~3 min. Usage: bash cut.sh
set -euo pipefail
FF=/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg
SRC="/Users/air/Downloads/Screen Recording 2026-11-06 181405.mp4"
DIR=$(cd "$(dirname "$0")" && pwd)
OUT=$DIR/seg; mkdir -p "$OUT"; rm -f "$OUT"/*
FONT=/System/Library/Fonts/HelveticaNeue.ttc
ENC=(-c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -r 30 -c:a aac -b:a 64k -ar 48000 -ac 2)

A="A · PhD stipend, three months late"
B="B · Nurse, third night shift in a row"
SUB_L="Live demo, 6 Nov 2026 · model waits cut"
REP="replies: with physio, then text-only"
MSG="user message + physio summary"
SETUP="scenario and options typed live"

# start|end|case|turn|sub|switch_at|turn2|sub2|mask
SEGS=(
"141.5|158.0|$A|Setup|$SETUP|9.0|Turn 1|$MSG|1"
"182.0|185.5|$A|Turn 1|$REP||||0"
"191.0|200.0|$A|Turn 2|$MSG||||0"
"224.0|227.5|$A|Turn 2|$REP||||0"
"233.5|242.5|$A|Turn 3|$MSG||||0"
"288.5|292.0|$A|Turn 3|$REP||||0"
"297.5|306.5|$A|Turn 4|$MSG||||0"
"336.5|340.0|$A|Turn 4|$REP||||0"
"344.0|353.0|$A|Turn 5|$MSG||||0"
"402.0|405.5|$A|Turn 5|$REP||||0"
"411.0|420.0|$A|Turn 6|$MSG||||0"
"460.0|469.0|$A|Turn 6|$REP||||0"
"519.5|523.5|$B|Setup|$SETUP||||0"
"531.5|546.0|$B|Setup|$SETUP|6.0|Turn 1|$MSG|0"
"564.0|567.5|$B|Turn 1|$REP||||0"
"572.0|581.0|$B|Turn 2|$MSG||||0"
"603.5|607.0|$B|Turn 2|$REP||||0"
"610.5|619.5|$B|Turn 3|$MSG||||0"
"646.5|652.0|$B|Turn 3|$REP||||0"
"669.0|678.0|$B|Turn 4|$MSG||||0"
"706.0|711.0|$B|Turn 4|$REP||||0"
"726.5|730.0|$B|Turn 5|$MSG||||0"
"799.0|813.0|$B|Turn 5|$REP|5.0|Turn 6|$MSG|0"
"843.5|856.0|$B|Turn 6|$REP||||0"
)

# drawtext reads text from files so the middle dots and commas need no escaping
txt() { local f; f=$(mktemp "$OUT/t.XXXXXX"); printf '%s' "$1" > "$f"; echo "$f"; }
dt() { # file size colour x y [enable]
  local e=""; [ -n "${6:-}" ] && e=":enable='$6'"
  echo "drawtext=fontfile=$FONT:textfile=$1:fontsize=$2:fontcolor=$3:x=$4:y=$5$e"
}

# title card
T1=$(txt "PhysioBase · live demo"); T2=$(txt "6 Nov 2026 · two scenarios, six turns each · waits for the model cut")
$FF -v error -f lavfi -i "color=c=0x291973:s=1920x840:d=3:r=30" -f lavfi -i "anullsrc=r=48000:cl=stereo" -t 3 \
  -vf "$(dt $T1 72 white '(w-tw)/2' 340),$(dt $T2 34 0xC9C3EE '(w-tw)/2' 440)" "${ENC[@]}" -y "$OUT/00.mp4"

i=0
for s in "${SEGS[@]}"; do
  IFS='|' read -r st en cs tn sb sw tn2 sb2 mask <<< "$s"
  i=$((i+1))
  fc=$(txt "$cs"); fl=$(txt "$SUB_L")
  vf="setpts=PTS-STARTPTS,crop=1920:720:0:300"
  # the model path (roll no.) sits at y 73-91 of the crop for the first 0.4 s, then scrolls up under 70
  [ "$mask" = 1 ] && vf="$vf,drawbox=x=0:y=0:w=1920:h=70:color=0x0C0C0C:t=fill,drawbox=x=0:y=0:w=1920:h=100:color=0x0C0C0C:t=fill:enable='lt(t,2.5)'"
  vf="$vf,pad=1920:840:0:120:color=0x291973,$(dt $fc 40 white 48 24),$(dt $fl 24 0xC9C3EE 48 78)"
  ft=$(txt "$tn"); fs=$(txt "$sb")
  if [ -n "$sw" ]; then
    ft2=$(txt "$tn2"); fs2=$(txt "$sb2")
    vf="$vf,$(dt $ft 40 0xF2C14E 'w-tw-48' 24 "lt(t,$sw)"),$(dt $fs 24 0xC9C3EE 'w-tw-48' 78 "lt(t,$sw)")"
    vf="$vf,$(dt $ft2 40 0xF2C14E 'w-tw-48' 24 "gte(t,$sw)"),$(dt $fs2 24 0xC9C3EE 'w-tw-48' 78 "gte(t,$sw)")"
  else
    vf="$vf,$(dt $ft 40 0xF2C14E 'w-tw-48' 24),$(dt $fs 24 0xC9C3EE 'w-tw-48' 78)"
  fi
  $FF -v error -ss "$st" -to "$en" -i "$SRC" -vf "$vf" -af "asetpts=PTS-STARTPTS" "${ENC[@]}" -y "$OUT/$(printf %02d $i).mp4"
done

ls "$OUT"/[0-9]*.mp4 | sed "s|^|file '|; s|$|'|" > "$OUT/list.txt"
$FF -v error -f concat -safe 0 -i "$OUT/list.txt" -c copy -movflags +faststart -y "$DIR/physiobase-demo.mp4"
