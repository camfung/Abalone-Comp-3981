### Abalone Comp 3981 

- Cameron Fung (A01268094)
- Elsa Ho (A01332339)
- Callum Goss (A01328294)
- Joseph Driedger (A01320740)

## Running the Game (pre-built)

1. Unzip the zip file
2. Open the `Abalone_Game` folder
3. Run `Abalone_Game.exe`
   - If a Windows security warning appears, click **More info → Run anyway**

## Building from Source

### Prerequisites

- Python 3.11
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) *(optional — only needed to produce a `.exe` installer)*

### Install dependencies

```bat
pip install -r requirements.txt
pip install pyinstaller
```

### Build

Run from the project root:

```bat
installer\build.bat
```

This produces:
- `dist\Abalone_Game\` — standalone folder (zip this to share the game)
- `dist\installer\Abalone_Game_Setup.exe` — Windows installer *(if Inno Setup is installed)*

### Run from source (no build)

```bat
python -m venv venv
.\venv\Scripts\activate.bat
pip install -r requirements.txt
python driver.py
```

![Screenshot](docs/diagram.png)
