#!/usr/bin/env python3

'''
Build script that generates common.css from modular CSS files in src/modules/
Each CSS file gets converted to an @import statement pointing to MediaWiki:Common-{filename}.css
'''

import os
import glob

def ensure_header_comment(file_path):
    """Ensure the file starts with the required MediaWiki comment"""
    required_header = "/* This is imported by MediaWiki:Common.css */"

    # Read the current file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if the file already has the required header
    if content.startswith(required_header):
        return False  # No changes needed

    # Add the header comment as the first line
    new_content = required_header + "\n" + content

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True  # File was modified

def build_common_css():
    """Generate common.css with @import statements for each module"""
    src_dir = "src"
    output_file = "common.css"
    header_text = """
/*

See https://github.com/RopeWiki/commoncss/ for details of how this file is generated
Please don't edit this file directly - it will be automatically overwritten.

The original monolithic file has been broken down into smaller, more manageable modules.
Content has been moved to the following files:

 * 01-typography.css - Font and heading styles
 * 02-layout.css - Basic layout and structural styles
 * 03-tables.css - Table styling
 * 04-forms-inputs.css - Form and input controls
 * 05-modals-popups.css - Modal and popup styles
 * 06-images-media.css - Image and media handling
 * 07-navigation-ui.css - Navigation and UI elements
 * 08-ratings-stars.css - Rating and star system
 * 09-maps-controls.css - Map controls and interactions
 * 10-conditions-weather.css - Conditions and weather styles
 * 11-canyon-display.css - Canyon display and permit styles
 * 12-utilities.css - Utility classes and common elements
 * 13-responsive.css - Responsive design and mobile styles
 * 14-icons-legacy.css - Legacy icons and condition icons

To add new styles, create them in the appropriate module file.
To build the final common.css, run: python3 build.py

*/

"""

    if not os.path.exists(src_dir):
        print(f"Error: {src_dir} directory not found")
        return

    # Find all CSS files in modules directory
    css_files = sorted(glob.glob(os.path.join(src_dir, "*.css")))

    if not css_files:
        print(f"No CSS files found in {src_dir}")
        return

    # Ensure all CSS files have the required header comment
    modified_files = []
    for css_file in css_files:
        if ensure_header_comment(css_file):
            modified_files.append(css_file)

    if modified_files:
        print(f"Added required header comment to {len(modified_files)} files:")
        for file in modified_files:
            print(f"  {file}")
    else:
        print("All files already have the required header comment")

    # Generate @import statements
    imports = [header_text]
    for css_file in css_files:
        # Extract filename without extension
        filename = os.path.splitext(os.path.basename(css_file))[0]

        # Create @import statement
        import_url = f'/MediaWiki:Common-{filename}.css?action=raw&ctype=text/css'
        import_statement = f'@import url("{import_url}");'
        imports.append(import_statement)

    # Write to common.css
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(imports) + '\n')

    print(f"Generated {output_file} with {len(imports)} imports:")
    for imp in imports:
        print(f"  {imp}")

if __name__ == "__main__":
    build_common_css()
