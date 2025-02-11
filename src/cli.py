import argparse
import google_sheets_manager
import pandas as pd


def cli_main():
    parser = argparse.ArgumentParser(description="Google Sheets CLI Utility")

    parser.add_argument("--clear-all", action="store_true", help="Clear all data including headers")
    parser.add_argument("--clear-keep-headers", action="store_true", help="Clear all rows but keep headers")
    parser.add_argument("--print-data-types", action="store_true", help="Print all data headers and their types")

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

    elif args.print_data_types:
        data = google_sheets_manager.fetch_google_sheets_data()
        if data:
            df = pd.DataFrame(data[1:], columns=data[0])
            print("📊 Data Headers and Their Types:")
            print(df.dtypes)
        else:
            print("❌ No data found in Google Sheets.")

    else:
        parser.print_help()


if __name__ == "__main__":
    cli_main()
