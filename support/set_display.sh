#!/bin/bash
/usr/bin/chmod 1777 /tmp/.X11-unix
export DISPLAY=${DISPLAY:-:0} # Select screen 0 by default.
xdpyinfo &>/dev/null && return
if command -v x11vnc &>/dev/null; then
  ! pgrep -a x11vnc && x11vnc -bg -forever -nopw -quiet -display WAIT$DISPLAY &
fi
! pgrep -a Xvfb && Xvfb $DISPLAY -screen 0 1024x768x16 &
sleep 1
if command -v fluxbox &>/dev/null; then
  ! pgrep -a fluxbox && fluxbox 2>/dev/null &
fi
echo "IP: $(hostname -I) ($(hostname))"

tail -f /dev/null
