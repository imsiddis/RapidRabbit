
# The Rapid Rabbit Toolkit README
Welcome to The Rapid Rabbit Toolkit, a lightweight and modular framework designed for cybersecurity professionals. This toolkit aims to simplify the integration and management of various cybersecurity tools, making your penetration testing workflow more efficient and adaptable.

## Description
The Rapid Rabbit Toolkit is a collection of scripts and tools designed to streamline the process of running and managing various cybersecurity tools. It provides a user-friendly interface for accessing and executing tools, as well as a modular structure for adding your own scripts and tools to the toolkit. The toolkit is designed to be easy to use and customizable, allowing you to tailor it to your specific needs and preferences.
<br>
It was developed as part of a cybersecurity dissertation project, and is intended to be a useful resource for cybersecurity professionals, students, and enthusiasts.
<br>
The toolkit is designed to run on any platform that supports Python, and is intended to be easy to install and use. It includes built-in functions for handling assets, such as creating and managing directories and files, and provides a clear and structured command-line interface for interacting with the toolkit.

## Getting Started
To get started with The Rapid Rabbit Toolkit, clone this repository to your local machine and ensure you have Python installed. The toolkit is designed to run on any platform that supports Python.

### Prerequisites
* Python 3.7 or later
* Basic knowledge of command-line interfaces
* Familiarity with Python scripting

### Usage
By design this toolkit is intended to be easy to run, and requires no installation. Simply clone the repository to your local machine and run the main.py script to start the toolkit. You can also add your own scripts and tools to the toolkit by following the guidelines in the "Adding Your Own Scripts" section below.
### Run the main script to start the toolkit:
* Open your terminal or command prompt and navigate to the directory where you cloned the repository.
* Run the main.py script using the following command:
```*bash
python3 /YourPathGoesHere/main.py
```
## Using The Rapid Rabbit Toolkit
Upon starting the toolkit, it will automatically detect and list available tools by scanning the tool_folder. The main menu will guide you through the various functionalities offered by the toolkit.

# Main Features
* **Script Discovery:** Automatically detects tools and scripts added to the toolkit for easy access.
* **User-Friendly Interface:** Interact with the toolkit through a clear and structured command-line interface.
* **Modular Design:** Easily add your own scripts and tools to the toolkit for a more personalized experience.
* **Built-In asset functions:** The toolkit includes built-in functions for handling assets, such as creating and managing directories and files.
* **Cross-Platform:** The toolkit is designed to run on any platform that supports Python.

### Adding Your Own Scripts

#### Script Import Wizard
As of the 15th of May, 2024 an interactive import script has been added to the framework. Instead of having to manually adding your own scripts with the risk of simple syntax mistakes, **"import.py"** will ensure that all the necessary fields has been added.

#### **Import Wizard Overview:**
* It will prompt the user for the necessary input requirements.
* It will then copy the python file to the tool folder, and then add the necessary meta data to the script by adding it after any imports that may be in the file and before the the first function in the script. This ensures that the integrity of the original file remains, instead of editing the original in case of an unforseen bug or user error. 

#### Manual Script Integration

To extend the functionality of The Rapid Rabbit Toolkit with your own scripts, follow these guidelines:

* **Prepare Your Script:** Ensure your script is written in Python and contains a tool_details dictionary at the top of the file with the following format:
``` *python
tool_details = {
    "name": "Your Tool Name", # The name of your tool. [REQUIRED]
    "filename": "your_tool_filename.py",  # The name of the file containing your tool. [REQUIRED]
    "category": "Your Tool Category", # [REQUIRED]
    "version": "Your Tool Version", # [RECOMMENDED]
    "description": "A brief description of what your tool does." # [REQUIRED]
}
```
It is recommended to place this at the top of your script to ensure that the toolkit can properly detect and display your tool effectively.

* **Ensure Proper main() Function:** Your script should contain a main() function that will be called when the tool is selected from the toolkit's main menu.
The main() function should be wrapped in an if __name__ == "__main__" block to ensure it is only called when the script is run directly. It should also contain a "while True" statement, to ensure that the script  
This is the preferred structure for your main() function.:

```*python
def main():
    print("Hello World!")

# -- Your Code Here -- #
if __name__ == "__main__":
    while True:
        main()
```
It is highly recommended to include a "try" and "except" block in your main() function to handle any exceptions that may occur during the execution of your script. This will help ensure that the toolkit remains stable and responsive.

* **Place Your Script:** Copy your script into the 'tool_folder' directory within the toolkit's structure.

* **Refresh The Toolkit:** To detect and integrate your new script, either restart the toolkit or press "Enter" a few times while in the main menu to refresh the tool and category lists.

### Adding your own wordlists
To add your own wordlists to the toolkit, follow these guidelines:
1. Ensure your wordlist is in a .txt format.
2. Place your wordlist in the 'wordlists' directory within the toolkit's root directory.<br>If it does not exist, create the 'wordlists' directory within the toolkit's structure.

# Troubleshooting
If you encounter any issues while using The Rapid Rabbit Toolkit, please refer to the following troubleshooting tips:
## Configuring Python Path

If you encounter a `ModuleNotFoundError` stating that the "internal_library" module is not found, you may need to adjust your Python path. Follow these steps to ensure Python can locate the module:

1. **Identify Your Python Executable:**

   Determine the path of the Python executable you're using. You can do this by running:

For Linux:
   ```bash
   which python3
   ```
2. **Set the PYTHONPATH Environment Variable:**

Next, add the root directory of this project to your PYTHONPATH environment variable. Replace /path/to/project with the actual path to the project's root directory.

On Unix-like systems (Linux/macOS):
Set PYTHONPATH temporarily by running the following in your terminal:

```bash
export PYTHONPATH="${PYTHONPATH}:PATH/TO/PROJECT"
```
On Windows:
Set PYTHONPATH temporarily by running the following in your terminal:

```bash
setx PYTHONPATH "%PYTHONPATH%;%cd%"
```

3. **Verify the PYTHONPATH:**
```bash	
python3 -c "import sys; print(sys.path)"
```
This command will print the current Python path. Verify that the project's root directory is included in the output.

## Reporting Issues
If you encounter any issues while using The Rapid Rabbit Toolkit, please open an issue in the GitHub repository. Be sure to include a detailed description of the problem, including any error messages or other relevant information. This will help us identify and resolve the issue as quickly as possible.

## Contributing
Contributions to The Rapid Rabbit Toolkit are welcome! Whether it's adding new features, improving existing tools, or reporting bugs, your input helps make this toolkit better for everyone.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Thanks to all contributors and users of The Rapid Rabbit Toolkit.
Special thanks to the cybersecurity community for inspiring the development of this toolkit.
For more information, feature requests, or to report bugs, please open an issue in the GitHub repository.