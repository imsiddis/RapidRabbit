from internal_library.asset_functions import clear_screen, beautify, beautify_string, beautify_title

tool_details = {
    "name":"about",
    "Category":"Information",
    "version":"1.0",
    "Description":"This will be the about section for the project."
}


def about():
    print('''
          # This function will contain the information contained in the about section. #         
    ''')

def main():
    clear_screen()
    about()

if __name__ == "__main__":
    main()