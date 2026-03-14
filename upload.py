#!/usr/bin/env python3

'''
Script to upload CSS files to MediaWiki pages.
- Uploads individual module files from src/modules/ to MediaWiki:Common-{filename}.css
- Uploads main common.css to MediaWiki:Common.css

Requires 3 envvars:
  MEDIAWIKI_SITE_URL (or use --prod flag for https://ropewiki.com)
  MEDIAWIKI_USERNAME
  MEDIAWIKI_PASSWORD

Requires the `mwclient` and `python-dotenv` pip packages.

Usage:
  ./upload.py                      # Upload to site specified in .env
  ./upload.py --prod               # Upload to production (ropewiki.com)
  ./upload.py --delete-unexpected  # Delete unexpected MediaWiki:Common... pages
  ./upload.py --help               # Show help message
'''

import mwclient
import os
import sys
import glob
import argparse
from dotenv import load_dotenv

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Upload CSS files to MediaWiki pages',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                      Upload to site specified in .env
  %(prog)s --prod               Upload to production (ropewiki.com)
  %(prog)s --delete-unexpected  Delete unexpected MediaWiki:Common... pages
        '''
    )
    parser.add_argument(
        '--prod',
        action='store_true',
        help='Upload to production (ropewiki.com) instead of dev site'
    )
    parser.add_argument(
        '--delete-unexpected',
        action='store_true',
        help='Delete unexpected MediaWiki:Common... pages (use with caution!)'
    )
    return parser.parse_args()

# Parse arguments
args = parse_args()

load_dotenv()

# Check for --prod flag
if args.prod:
    site_url = 'https://ropewiki.com'
    print("🚀 Production mode: uploading to ropewiki.com")
else:
    site_url = os.getenv("MEDIAWIKI_SITE_URL")

username, password = (
    os.getenv(var)
    for var in ["MEDIAWIKI_USERNAME", "MEDIAWIKI_PASSWORD"]
)

if not all([site_url, username, password]):
    sys.exit(
        "Error: Ensure MEDIAWIKI_SITE_URL, MEDIAWIKI_USERNAME, and MEDIAWIKI_PASSWORD are all set."
    )

print(f"Target: {site_url}")

# Strip protocol from URL if present
site_url = site_url.replace("https://", "").replace("http://", "")

site = mwclient.Site(site_url, path="/")
site.login(username, password)

def upload_file(file_path, page_name, edit_summary="build sync"):
    """Upload a single file to a MediaWiki page"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            new_content = file.read()

        page = site.pages[page_name]
        page.edit(new_content, summary=edit_summary)
        print(f"✓ Uploaded {file_path} to {page_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to upload {file_path} to {page_name}: {e}")
        return False

def check_for_unexpected_common_pages(delete_unexpected=False):
    """Check for MediaWiki:Common... pages that aren't part of this build process

    Args:
        delete_unexpected: If True, delete unexpected pages (default: False)
    """
    print("Checking for unexpected MediaWiki:Common... pages...")

    # Get expected pages based on current build
    expected_pages = {"MediaWiki:Common.css"}

    # Allow list of known pages that aren't part of the build process
    allowed_unexpected = {
        "MediaWiki:Common.js"
    }

    # Add expected module pages
    src_dir = "src"
    if os.path.exists(src_dir):
        css_files = sorted(glob.glob(os.path.join(src_dir, "*.css")))
        for css_file in css_files:
            filename = os.path.splitext(os.path.basename(css_file))[0]
            expected_pages.add(f"MediaWiki:Common-{filename}.css")

    # Query all pages starting with "MediaWiki:Common"
    try:
        # Use a more specific approach - search for pages in MediaWiki namespace
        # and filter by title pattern
        all_common_pages = []
        for page in site.allpages(namespace=8):  # MediaWiki namespace is 8
            if page.page_title.startswith("Common"):
                all_common_pages.append(page)

        found_pages = {f"MediaWiki:{page.page_title}" for page in all_common_pages}

        # Find unexpected pages (excluding allowed ones)
        unexpected_pages = found_pages - expected_pages - allowed_unexpected

        if unexpected_pages:
            print(f"⚠️  WARNING: Found {len(unexpected_pages)} unexpected MediaWiki:Common... page(s):")
            for page_name in sorted(unexpected_pages):
                print(f"   - {page_name}")

            if delete_unexpected:
                print()
                print("🗑️  Deleting unexpected pages...")
                deleted_count = 0
                for page_name in sorted(unexpected_pages):
                    try:
                        page = site.pages[page_name]
                        page.delete(reason="Orphaned page - not part of current build process")
                        print(f"   ✓ Deleted: {page_name}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"   ✗ Failed to delete {page_name}: {e}")

                print(f"\n✓ Deleted {deleted_count}/{len(unexpected_pages)} unexpected pages")
                return True
            else:
                print("   These pages may be orphaned or not part of the current build process.")
                print("   Use --delete-unexpected flag to remove them.")
                return False
        else:
            print("✓ No unexpected MediaWiki:Common... pages found")
            return True

    except Exception as e:
        print(f"✗ Failed to check for unexpected pages: {e}")
        return False

def main():
    success_count = 0
    total_count = 0

    # Upload individual module files
    src_dir = "src"
    if os.path.exists(src_dir):
        css_files = sorted(glob.glob(os.path.join(src_dir, "*.css")))
        for css_file in css_files:
            filename = os.path.splitext(os.path.basename(css_file))[0]
            page_name = f"MediaWiki:Common-{filename}.css"
            total_count += 1
            if upload_file(css_file, page_name):
                success_count += 1

    # Upload main common.css
    if os.path.exists("common.css"):
        total_count += 1
        if upload_file("common.css", "MediaWiki:Common.css"):
            success_count += 1
    else:
        print("Warning: common.css not found. Run build.py first.")

    print(f"\nUpload complete: {success_count}/{total_count} files uploaded successfully")

    # Check for unexpected Common pages after upload
    print()  # Add spacing
    check_result = check_for_unexpected_common_pages(delete_unexpected=args.delete_unexpected)

    if not check_result and not args.delete_unexpected:
        print("\n⚠️  WARNING: Unexpected MediaWiki:Common... pages were found (see above)")

if __name__ == "__main__":
    main()
