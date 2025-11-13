# CMS Documentation Common Configuration

Shared configuration and assets for CMS documentation sites using the [mkdocs-header-dropdown-plugin](https://github.com/cms-cat/mkdocs-header-dropdown-plugin).

## Contents

- **header-dropdown.yml**: Standard CMS POG documentation dropdown configuration with nested menus
- **pog-docs.yml**: Authoritative list of POG documentation URLs (structured data)
- **pog_docs_loader.py**: Python utility to load POG docs into dataclasses (for backward compatibility)
- **CMSlogo_white_nolabel_1024_May2014.png**: CMS logo for header dropdown

## Usage

### As a Git Submodule

Add this repository as a git submodule in your documentation repository:

```bash
cd your-docs-repo
git submodule add https://github.com/cms-cat/cms-docs-common.git
```

Then reference it in your `mkdocs.yml`:

```yaml
plugins:
  - header-dropdown:
      config_file: "cms-docs-common/header-dropdown.yml"
```

And add the CMS logo to your `extra_css` or copy it to your assets:

```bash
cp cms-docs-common/CMSlogo_white_nolabel_1024_May2014.png docs/assets/
```

### Updating

To update to the latest shared configuration:

```bash
git submodule update --remote cms-docs-common
```

## Customization

You can extend the shared configuration with repository-specific dropdowns:

```yaml
plugins:
  - header-dropdown:
      config_file: "cms-docs-common/header-dropdown.yml"
      dropdowns:
        - title: "Project Specific"
          links:
            - text: "Project Wiki"
              url: "https://example.com"
```

## POG Documentation URLs

### Using in MkDocs (Header Dropdown)

The POG documentation is automatically included in `header-dropdown.yml` with clickable parent links and nested submenus for Run2/Run3/era-specific docs.

### Using in Python Code

For backward compatibility with existing code that uses POG_DOCS dataclasses:

```python
from pog_docs_loader import POG_DOCS, Docs

# Access POG documentation
btv_docs = POG_DOCS["BTV"]
print(btv_docs.fallback)  # https://btv-wiki.docs.cern.ch/
print(btv_docs.Run2)       # None (BTV doesn't have Run2/Run3 split)
print(btv_docs.era["Run3-22CDSep23-Summer22-NanoAODv12"])  # Era-specific URL
```

### Updating POG Documentation

To add or update POG documentation URLs, simply edit `pog-docs.yml`:

1. **Edit `pog-docs.yml`** - This is the single source of truth
2. **Commit the file** - Dropdown links auto-generate, Python code auto-loads

The dropdown plugin automatically generates nested menus from the YAML structure using the `auto_generate_from` feature.

Structure in `pog-docs.yml`:
```yaml
pog_docs:
  POG_NAME:
    fallback: "https://..."  # Used as clickable parent URL
    Run2: "https://..."      # Creates "Run2" submenu item
    Run3: "https://..."      # Creates "Run3" submenu item
    era:                     # Nested dict creates submenu
      era-name: "https://..."
```

The plugin recognizes special keys:
- `fallback` or `url`: Makes the parent item clickable
- Other string values: Create submenu items
- Nested dicts: Create nested submenus

More info: https://cms-analysis-corrections.docs.cern.ch/development/

## Maintaining

To update the shared configuration, edit `header-dropdown.yml` and/or `pog-docs.yml` in this repository and commit. All documentation sites using this as a submodule can then pull the updates.
