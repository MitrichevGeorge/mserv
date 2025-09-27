#!/bin/sh
set -eu

cd "$HOME"
mkdir -p .mserv
cd .mserv

wget -q https://github.com/MitrichevGeorge/mserv/archive/refs/heads/main.zip -O mserv.zip
unzip -q mserv.zip
mv mserv-main/* .
mv mserv-main/.* . 2>/dev/null || true
rm -rf mserv-main mserv.zip

chmod +x run.sh
[ ! -f id ] && uuidgen > id

python -m venv e

"$HOME/.mserv/e/bin/pip" install --upgrade pip
"$HOME/.mserv/e/bin/pip" install pyautogui requests

BIN="$HOME/bin"
M_CMD="$BIN/m"

mkdir -p "$BIN"

cat > "$M_CMD" <<'EOF'
#!/bin/sh
# Команда m — запускает ~/.mserv/run.sh через venv
exec "$HOME/.mserv/e/bin/python" "$HOME/.mserv/run.sh" "$@"
EOF
chmod +x "$M_CMD"

case ":$PATH:" in
  *":$BIN:"*)
    printf "Каталог %s уже в PATH — можете запускать команду: m\n" "$BIN"
    ;;
  *)
    # bashrc
    if [ -w "$HOME/.bashrc" ] || [ ! -e "$HOME/.bashrc" ]; then
      if ! grep -Fqx 'export PATH="$HOME/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
        printf "\n# добавить ~/bin в PATH, создано скриптом make_m.sh\nexport PATH=\"$HOME/bin:\$PATH\"\n" >> "$HOME/.bashrc"
        printf "Добавил строку в %s для постоянного добавления ~/bin в PATH.\n" "$HOME/.bashrc"
      fi
    fi
    # profile
    if [ -w "$HOME/.profile" ] || [ ! -e "$HOME/.profile" ]; then
      if ! grep -Fqx 'export PATH="$HOME/bin:$PATH"' "$HOME/.profile" 2>/dev/null; then
        printf "\n# добавить ~/bin в PATH, создано скриптом make_m.sh\nexport PATH=\"$HOME/bin:\$PATH\"\n" >> "$HOME/.profile"
        printf "Добавил строку в %s.\n" "$HOME/.profile"
      fi
    fi
    printf "Чтобы использовать команду прямо сейчас:\n\n  source ~/.bashrc\n\nили откройте новый терминал.\n"
    ;;
esac

AUTOSTART="$HOME/.config/autostart"
mkdir -p "$AUTOSTART"

cat > "$AUTOSTART/mserv.desktop" <<EOF
[Desktop Entry]
Type=Application
Exec=bash -c 'source \$HOME/.mserv/e/bin/activate && \$HOME/.mserv/run.sh'
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=MServ
Comment=Запуск MServ после старта KDE
EOF

printf "Добавил автозапуск GUI: %s/mserv.desktop\n" "$AUTOSTART"
