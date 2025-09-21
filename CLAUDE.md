# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository manages CSS for a MediaWiki site. The CSS is maintained as a single file (`common.css`) that gets uploaded to the MediaWiki:Common.css page on the target site.

## Architecture

The current structure is a single monolithic CSS file approach, but the user has indicated they want to transition to a modular system where CSS is constructed from multiple smaller, manageable files.

### Current Files

- `common.css` - The main CSS file containing all styles (3172+ lines)
- `upload.py` - Python script for uploading CSS to MediaWiki site
- `CLAUDE.md` - This documentation file

### CSS Structure Analysis

The current `common.css` contains:
- Font imports (Google Fonts)
- Table styling (sticky headers, wikitable styles)
- UI components (canyon popup, legends, diff views)
- Responsive design elements
- MediaWiki-specific overrides

## Common Commands

### Upload CSS to MediaWiki
```bash
python3 upload.py
```

Requires environment variables:
- `MEDIAWIKI_SITE_URL`
- `MEDIAWIKI_USERNAME`
- `MEDIAWIKI_PASSWORD`

Dependencies: `mwclient` Python package

### View CSS file size
```bash
wc -l common.css
```

## Development Workflow

When making changes:
1. Edit the `common.css` file directly (current approach)
2. Test changes locally if possible
3. Use `upload.py` to deploy to MediaWiki site

## Future Architecture Goal

The user wants to refactor this into a modular system where:
- CSS is split into multiple smaller, manageable files
- Files are concatenated/built into a single `common.css` for upload
- This would require implementing a build system

## MediaWiki CSS Considerations

- CSS must be compatible with MediaWiki's CSS loading system
- Styles apply to all skins unless specifically targeted
- Font imports must be first in the file
- Some styles target MediaWiki-specific classes and IDs