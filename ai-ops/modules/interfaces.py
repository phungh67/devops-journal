import sys
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from utils.templater import template_loader
from utils.verifier import verify_template

def handle_view_profile():
    print("\n--- User Profile ---")
    print("Status: Active")
    print("Permissions: Administrator\n")

def handle_configure_settings():
    # Multi-select checkbox menu
    features = inquirer.checkbox(
        message="Toggle system features (Space to select, Enter to confirm):",
        choices=["Dark Mode", "Auto-Save", "Telemetry Notifications", "Beta Features"],
    ).execute()
    print(f"Updated preferences: {features}\n")

def handle_Submit_bug():
    # Validated text input
    issue = inquirer.text(
        message="Describe the issue:",
        validate=EmptyInputValidator("Description cannot be empty!"),
    ).execute()
    print(f"Ticket submitted successfully for: '{issue}'\n")

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
