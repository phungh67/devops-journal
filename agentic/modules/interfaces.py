import sys
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from utils.templater import template_loader
from utils.verifier import verify_template


def main():
    print("====================================")
    print("    WELCOME TO THE SYSTEM PORTAL    ")
    print("====================================\n")

    while True:
        # Main menu keyboard-navigable dropdown
        action = inquirer.select(
            message="Select an action:",
            choices=[
                "View Profile",
                "Configure Settings",
                "Submit Bug Report",
                "Exit Application"
            ],
            default="View Profile",
        ).execute()

        if action == "View Profile":
            handle_view_profile()
        elif action == "Configure Settings":
            handle_configure_settings()
        elif action == "Submit Bug Report":
            handle_Submit_bug()
        elif action == "Exit Application":
            print("Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
