#!/bin/bash

deviceid=`xinput | grep "Touchpad" | awk -F" " {'print $6'} | awk -F"=" {'print $2'}`
propid=`xinput list-props ${deviceid} | grep "libinput Tapping Enabled (" | awk -F" " {'print $4'}`
propid=${propid:1:3}
xinput set-prop ${deviceid} ${propid} 1
