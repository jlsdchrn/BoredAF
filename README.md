# Project: BoredAF - Surviving CISD

## Overview
This project includes scripts to enhance your productivity (or sanity) during CISD. With tools to display real-time progress and entertaining visuals, BoredAF brings some much-needed relief to your schedule.

## Features
- **Calendar Integration:** Extracts schedule data from an `.ics` file.
- **Progress Visualization:** Displays your CISD progress with the `rich` library.
- **Dynamic UI:** Includes an ASCII-rendered GIF for a fun twist.
- **Convenient Alias:** Use a custom shell alias (`hateCISD`) to quickly run the program.

---

## Installation Guide

### Prerequisites
- Python 3.6+
- `pip` installed

### Setup Instructions
1. Clone or download the project to your home directory:
   ```bash
   cd ~
   git clone https://github.com/jlsdchrn/BoredAF.git
   cd BoredAF
   ```

2. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```

3. Run the setup script, specifying your shell (bash or zsh):
   ```bash
   ./setup.sh [bash|zsh]
   ```

   This script will:
   - Create a Python virtual environment `BordedAF_env` in your home directory.
   - Install the required dependencies (`rich`, `ics`, `Pillow`, `beautifulsoup4`, `requests`).
   - Add the `hateCISD` alias to your shell configuration file.

4. Reload your shell configuration:
   ```bash
   source ~/.bashrc   # for bash
   source ~/.zshrc    # for zsh
   ```

---

## Usage

### Running the Script
1. Ensure your `BoredAF` directory contains:
   - `wanna_quit_my_major.py`: Main script.
   - `animated_gif.py`: Utility for processing GIFs.

2. Prepare your `.ics` calendar file (e.g., `ADECal.ics`) and place it in the `BoredAF` directory. 
If the name is different from `ADECal.ics`, change it in the code.

3. Run the program using the alias:
   ```bash
   hateCISD
   ```

   Additional options for the script can be passed as arguments to the alias.

### Customizing the GIF
- The script automatically downloads or uses existing GIFs from the `gif/` folder.
- To specify a custom GIF:
   ```bash
   hateCISD --url <gif-url> --name <gif-name>
   ```


### Customizing the project
- You can modify the text you want to be displayed by modifying the values of the 'Prompt' class in the 'wanna_quit_my_major.py'
- You can change the name **CISD** by the name of your major in the program.

---

## File Structure
- `wanna_quit_my_major.py`: Core logic for calendar parsing and UI rendering.
- `animated_gif.py`: GIF downloading and ASCII conversion utility.
- `setup.sh`: Installation script for environment setup and alias configuration.
- `gif/`: Directory for storing GIFs used by the script.

---

## Troubleshooting
- **Virtual Environment Issues:**
  If the virtual environment fails to activate, ensure `python3-venv` is installed on your system:
  ```bash
  sudo apt install python3-venv
  ```

- **Dependency Errors:**
  Re-run the setup script to reinstall dependencies:
  ```bash
  ./setup.sh [bash|zsh]
  ```

- **Alias Not Working:**
  Double-check your shell configuration file and source it again:
  ```bash
  source ~/.bashrc   # for bash
  source ~/.zshrc    # for zsh
  ```

---

## Credits
- Inspired by the struggle of surviving CISD classes.
- ASCII rendering powered by the `Pillow` library.
- Interactive UI created with the `rich` Python library.

---

## License
This project is licensed under the MIT License.



