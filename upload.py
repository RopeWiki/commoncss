#!/usr/bin/env python3

'''
Script to upload CSS files to MediaWiki pages.
- Uploads individual module files from src/modules/ to MediaWiki:Common-{filename}.css
- Uploads main common.css to MediaWiki:Common.css

Requires 3 envvars:
  MEDIAWIKI_SITE_URL
  MEDIAWIKI_USERNAME
  MEDIAWIKI_PASSWORD

Requires the `mwclient` pip package.
'''

import mwclient
import os
import sys
import glob

site_url, username, password = (
    os.getenv(var)
    for var in ["MEDIAWIKI_SITE_URL", "MEDIAWIKI_USERNAME", "MEDIAWIKI_PASSWORD"]
)

if not all([site_url, username, password]):
    sys.exit(
        "Error: Ensure MEDIAWIKI_SITE_URL, MEDIAWIKI_USERNAME, and MEDIAWIKI_PASSWORD are all set."
    )

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

if __name__ == "__main__":
    main()
