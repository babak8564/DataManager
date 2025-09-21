
-----

### Secure Your Digital Life 🔐

This application provides a **secure and convenient way** to manage your sensitive information, including usernames, passwords, private keys, seed phrases, and important notes. It's a personal vault for your most crucial data.

-----

### Features

This app is built with user control and convenience in mind, offering a range of customizable features:

  * **Personalization**: You can customize the app's appearance by changing its **size**, **color**, and **style** to suit your preferences.
  * **Enhanced Security**:
      * Set an inactivity timer to **automatically log you out** after a period of idleness.
      * Enable a timer to **clear your clipboard** automatically after you copy a password, preventing sensitive data from being left in memory.
  * **Data Management**:
      * **Import** your data from external files. The app supports importing from **text files** (with a specified separator) and **CSV files** with two to four columns.
      * **Export** your data for backup or transfer.
  * **Database Control**: You have the flexibility to **change the name and directory** of your database file.

-----

### Getting Started

#### Prerequisites

  * **Python 3.10.0** or a higher version.

#### Installation

Follow these simple steps to get the application up and running:

1.  **Install Python 3.10.0** or a more recent version if you don't have it already.
2.  **Create a virtual environment** to keep project dependencies isolated:
    ```bash
    python3.10.0 -m venv venv
    ```
3.  **Activate the virtual environment**:
      * On **Linux/macOS**:
        ```bash
        source venv/bin/activate
        ```
      * On **Windows**:
        ```bash
        venv\Scripts\activate
        ```
4.  **Install the required dependencies** from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

#### Usage

Once the dependencies are installed, you can start the application by running:

```bash
python app.py
```

