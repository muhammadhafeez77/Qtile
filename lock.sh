##!/bin/bash
#t
is_media_playing() {
    command -v playerctl &>/dev/null && playerctl status 2>/dev/null | grep -q "Playing"
}

while is_media_playing; do
    sleep 15
done


# Clear hung instances safely
killall i3lock 2>/dev/null

SOURCE_PIC="${HOME}/Pictures/0-black-moon.jpg"
READY_BG="/tmp/current_lock_screen.png"

# CRITICAL SPEED FIX: Only convert if the file was updated or missing
if [ ! -f "$READY_BG" ] || [ "$SOURCE_PIC" -nt "$READY_BG" ]; then
    convert "$SOURCE_PIC" "$READY_BG"
fi

# Color configurations (#RRGGBBAA format)
BACKGROUND_COLOR='#11111b' # Dark fallback color
BAR_COLOR='#31324466'    
TYPING_COLOR='#89b4faff' 
WRONG_COLOR='#f38ba8ff'  
TEXT_COLOR='#cdd6f4ff'   

# Launch using --fill to stretch the image to the exact borders of your screen
/usr/bin/i3lock \
-c $BACKGROUND_COLOR \
--image="$READY_BG" \
--fill \
--clock \
--bar-indicator \
--bar-orientation="horizontal" \
--bar-pos="y+h-15" \
--bar-max-height="15" \
--bar-base-width="15" \
--bar-color=$BAR_COLOR \
--keyhl-color=$TYPING_COLOR \
--bshl-color=$WRONG_COLOR \
--wrong-color=$WRONG_COLOR \
--verif-color=$TEXT_COLOR \
--time-color=$TEXT_COLOR \
--date-color=$TEXT_COLOR \
--time-str="%I:%M %p" \
--date-str="%A, %d-%m-%Y" \
--time-size=42 \
--date-size=16 \
--time-pos="w/2:h/2-140" \
--date-pos="w/2:h/2-100" \
--verif-text="Checking password..." \
--wrong-text="Incorrect Password"


