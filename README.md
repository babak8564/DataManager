
-----

### Secure Your Digital Life 🔐

This application provides a **secure and convenient way** to manage your sensitive information, including usernames, passwords, private keys, seed phrases, and important notes. It's a personal vault for your most crucial data.

-----

### Features

This app is built with user control and convenience in mind, offering a range of customizable features:

  * **Personalization**: Customize the app's appearance by changing its **size**, **color**, and **style** to suit your preferences.


  * **Enhanced Security**:
      * Set an inactivity timer to **automatically log you out** after a period of idleness.
      * Enable a timer to **clear your clipboard** automatically after you copy a password, preventing sensitive data from being left in memory.
  * **Data Management**:
      * **Import** data from external files. The app supports importing from **text files** (with a specified separator) and **CSV files** with two to four columns.
      * **Export** your data for backup or transfer.
  * **Database Control**: Change the name and directory of your database file.

-----

### Getting Started

#### Prerequisites

  * **Python:** Version 3.10.0 or higher.
  * **Git:** For cloning the repository.
  * **Platform-Specific Dependencies:**
    * **Windows:** Windows: No additional system packages are required; tkinter and pyperclip are handled via pip.
    * **Linux (Ubuntu/Debian):** 
      * Install tkinter for the GUI:
      ```bash
      sudo apt-get install python3-tk
      ```
      * Install xclip for pyperclip clipboard functionality:
      ```bash
      sudo apt-get install xclip
      ```
      * macOS: 
      tkinter: Usually included with Python. If not, install via Homebrew:
      ```bash
      brew install python-tk
      ```
      * pyperclip: No additional system packages required; it works natively.

#### Installation

Follow these steps to set up the application:

1. **Create a project folder (optional):**
   ```bash
   mkdir your-folder_name
   cd your-folder_name

2. **Clone the repository**:
    ```bash
    git clone https://github.com/babak8564/Pass_Keeper.git
    cd Pass_Keeper
    ```

3.  **Ensure Python 3.10.0 or higher is installed:**
    If you need help installing a specific Python version, consult your package manager or ask an AI assistant.

4.  **Create a virtual environment** to keep project dependencies isolated:
    ```bash
    python -m venv virtual_e
    ```
    *Replace virtual_e with your preferred name.

5.  **Activate the virtual environment:**:
      * On **Linux/macOS**:
        ```bash
        source virtual_e/bin/activate
        ```
      * On **Windows**:
        ```bash
        virtual_e\Scripts\activate
        ```
6.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

#### Usage

Start the application by running:
  ```bash
  python app.py
  ```

