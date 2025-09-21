#!/usr/bin/env python3

'''
Build script that generates common.css from modular CSS files in src/modules/
Each CSS file gets converted to an @import statement pointing to MediaWiki:Common-{filename}.css
'''

import os
import glob

def build_common_css():
    """Generate common.css with @import statements for each module"""
    src_dir = "src"
    output_file = "common.css"
    header_text = """
/* See https://github.com/RopeWiki/commoncss/ for details of how this file is generated
   Please don't edit this file directly - it will be automatically overwritten.  */
""".strip()

    if not os.path.exists(src_dir):
        print(f"Error: {src_dir} directory not found")
        return

    # Find all CSS files in modules directory
    css_files = sorted(glob.glob(os.path.join(src_dir, "*.css")))

    if not css_files:
        print(f"No CSS files found in {src_dir}")
        return

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
