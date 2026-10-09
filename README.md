# Whale Girl Pet 🐋

A transparent, always-on-top **whale-girl desktop pet** for Windows, macOS and Linux,
built with Electron.

She floats on your desktop, bobs gently, and keeps you company. **Double-click her**
and she becomes a dictionary: free dictionaries answer first, and DeepSeek's model
takes over when they come up short.

<!-- Drop a screenshot at assets/screenshot.png and uncomment this line. -->
<!-- ![Whale Girl Pet](assets/screenshot.png) -->

## Features

| | |
|---|---|
| 🐋 **Desktop pet** | Transparent frameless window, always on top, drag her anywhere. She bobs, jumps when clicked, and cycles through idle lines. |
| 🖱️ **Click-through** | The transparent area passes mouse events straight through to whatever is behind her. She only takes the mouse when you hover her or a button. |
| 📖 **Term lookup** | Double-click her, type a word or term, press Enter. |
| 🎭 **Galgame dialogue bar** | Longer answers open in a bottom-screen dialogue box with a character portrait, in classic visual-novel style. |
| 💡 **Screenshot translation** | Click 💡, paste a screenshot (`Ctrl+V`), press Enter — she reads the image and translates/explains it. |
| 📓 **Word list** | Every lookup is collected, drag to reorder, and optionally appended to a `.txt` file you choose. |
| 📁 **Folder button** | Opens a folder of your choice — click to open, right-click to pick a different one. |
| 🔑 **API key box** | In-app settings for your DeepSeek key (stored locally, never sent anywhere else). |

## How lookup works

The lookup is **cheap-first**, so most words cost nothing and need no API key:

```
1. api.dictionaryapi.dev     free, no key
2. en.wiktionary.org         free, no key
3. DeepSeek model            fallback — needs a key
```

If both free dictionaries miss, the English definition they returned is translated to
Chinese; if there is nothing to translate, DeepSeek explains the term directly.

> Only step 3 needs an API key. Get one at
> [platform.deepseek.com](https://platform.deepseek.com), then paste it into the 🔑 box.

## Install

Requires [Node.js](https://nodejs.org/) 18+.

```bash
git clone https://github.com/lerongnovelmusic/whale-girl-pet.git
cd whale-girl-pet
npm install
npm start
```

`npm install` downloads Electron (~200 MB) once.

## Usage

| Action | Result |
|---|---|
| **Drag** her | Move her anywhere; the position is remembered |
| **Single click** | She jumps and says something |
| **Double click** | Opens the term input |
| **Type + Enter** | Look the term up |
| **💡** | Paste-screenshot mode: `Ctrl+V` then `Enter` |
| **📁** left / right click | Open the folder / choose a different folder |
| **🔑** | Set or clear your DeepSeek API key |
| **×** | Quit |

Press `Esc` to leave paste mode or close the key box.

## Configuration

Everything the app persists lives in
`%APPDATA%\whale-girl-pet` (Windows), `~/Library/Application Support/whale-girl-pet`
(macOS) or `~/.config/whale-girl-pet` (Linux):

- `window-pos.json` — last window position
- `Local Storage/` — your API key, word list, chosen folder, and window visibility

To start over, quit the app and delete that directory.

### Changing the models

`index.html` holds the model ids:

- `deepseek-chat` — text explanations and translations
- `deepseek-v4-flash-vision-exp` — screenshot (vision) input

## Project layout

```
main.js                  Electron main process: windows, IPC, drag, mouse pass-through
index.html               The pet: markup, styles, and all renderer logic
dialogue.html            Bottom galgame dialogue bar (self-contained, art inlined)
assets/icon.png|.ico     App / taskbar icon
tools/make_icon.py       Regenerates the icon from a sprite (needs Pillow)
```

## Regenerating the icon

```bash
pip install Pillow
python tools/make_icon.py
```

Edit the `SRC` path at the top of the script to point at your own sprite.

## Troubleshooting

**She exits immediately with `TypeError: Cannot read properties of undefined (reading 'on')`.**

Your environment has `ELECTRON_RUN_AS_NODE=1` set. That variable makes `electron.exe`
run as plain Node, so `require("electron")` returns a path string instead of the API.
This happens when you launch the pet from another Electron app's integrated terminal.
Clear it first:

```powershell
# Windows
$env:ELECTRON_RUN_AS_NODE = ""
npm start
```

```bash
# macOS / Linux
unset ELECTRON_RUN_AS_NODE
npm start
```

**No definitions at all.** The two free dictionary APIs need internet access. Behind a
proxy, or offline, every lookup falls through to DeepSeek and needs a valid key.

**`npm start` opens nothing.** Check that `npm install` completed; `node_modules/electron/dist`
must exist.

## License

The source code is [MIT](LICENSE).

The whale-girl character artwork (`index.html` and `dialogue.html` embed it, plus
`galgame-cover-small.jpg`) is the original creator's work, included for use with this
pet. If you fork this project, replace it unless you hold the rights to it.

## Contributing

Issues and pull requests are welcome. If you change the renderer, please test the
mouse pass-through behaviour — it is the easiest thing to break, and the failure mode
is a window you cannot click.
