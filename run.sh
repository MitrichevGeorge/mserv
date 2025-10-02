#!/bin/sh

cd ~/.mserv

LOCAL_VER_FILE="ver"
REMOTE_VER_URL="https://raw.githubusercontent.com/MitrichevGeorge/mserv/main/ver"

LOCAL_VER=$(cat "$LOCAL_VER_FILE")
REMOTE_VER=$(curl -fsSL "$REMOTE_VER_URL")

if [ "$LOCAL_VER" != "$REMOTE_VER" ]; then
  MAIN_PID=$$
  TMPFILE=$(mktemp /tmp/myscript.XXXXXX.sh)

cat > "$TMPFILE" <<EOF
#!/bin/sh
while kill -0 $MAIN_PID 2>/dev/null; do
    sleep 0.01
done

rm ~/.mserv
curl -fsSL https://raw.githubusercontent.com/MitrichevGeorge/mserv/main/install.sh | bash

rm -- "\$0"
EOF
  
  chmod +x "$TMPFILE"
  
  "$TMPFILE" &
  
  exit 0
fi

source e/bin/activate
python server.py
