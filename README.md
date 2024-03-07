### Abalone Comp 3981 

- Cameron Fung 
- Elsa Ho
- Callum Goss
- Joseph Driedger

## How to Run

Follow these steps to set up and run the program:

1. **Create a Virtual Environment:**
    - Run the following command to create a virtual environment:
        ```bash
        python -m venv venv
        ```

2. **Activate the Virtual Environment:**
    - On Windows:
        ```bash
        .\venv\Scripts\activate.bat
        ```
    - On Unix:
        - Provide execute permissions to the activate script:
            ```bash
            chmod u+x venv/bin/activate
            ```
        - Activate the virtual environment:
            ```bash
            source venv/bin/activate
            ```

3. **Install Dependencies:**
    - Run the following command to install the required dependencies:
        ```bash
        pip install -r requirements.txt
        pip install pyinstaller
        ```

4. **Export Python Driver to Executable File:**
    - Execute the program using the following command:
        ```
        pyinstaller driver.py --onefile --noconsole
        ```

5. **Copy assets to correct**
    - Copy the following folders into ./dist
        - formations
        - games
        - images

6. **Run the program and Have Fun.**
    - Open the dist directory
    - Open driver.exe
  
![Screenshot](docs/diagram.png)


