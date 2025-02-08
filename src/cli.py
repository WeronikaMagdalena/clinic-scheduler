import argparse
import google_sheets_manager


def cli_main():
    parser = argparse.ArgumentParser(description="Google Sheets CLI Utility")

    parser.add_argument("--clear-all", action="store_true", help="Clear all data including headers")
    parser.add_argument("--clear-keep-headers", action="store_true", help="Clear all rows but keep headers")

    args = parser.parse_args()

    if args.clear_all:
        confirm = input("⚠️ Are you sure you want to clear ALL data including headers? (yes/no): ").strip().lower()
        if confirm == "yes":
            if google_sheets_manager.clear_google_sheets(keep_headers=False):
                print("✅ Google Sheets fully cleared (headers removed).")
            else:
                print("❌ Failed to clear Google Sheets.")
        else:
            print("⏳ Operation canceled.")

    elif args.clear_keep_headers:
        confirm = input("⚠️ Are you sure you want to clear all rows but keep headers? (yes/no): ").strip().lower()
        if confirm == "yes":
            if google_sheets_manager.clear_google_sheets(keep_headers=True):
                print("✅ Google Sheets cleared (headers kept).")
            else:
                print("❌ Failed to clear Google Sheets.")
        else:
            print("⏳ Operation canceled.")

    else:
        parser.print_help()


if __name__ == "__main__":
    cli_main()
