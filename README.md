# CMS Documentation Common Configuration

Shared configuration and assets for CMS documentation sites using the [mkdocs-header-dropdown-plugin](https://github.com/cms-cat/mkdocs-header-dropdown-plugin).

## Contents

- **header-dropdown.yml**: Standard CMS POG documentation dropdown configuration with nested menus
- **pog-docs.yml**: Authoritative list of POG documentation URLs (structured data)
- **pog_docs_loader.py**: Python utility to load POG docs into dataclasses (for backward compatibility)
- **CMSlogo_white_nolabel_1024_May2014.png**: CMS logo for header dropdown

## Usage

### Include the GitLab CI Template

In your project's `.gitlab-ci.yml`, add:

```yaml
include:
  - project: 'cms-analysis/services/cms-docs-common'
    file: 'mkdocs-gitlab-pages.gitlab-ci.yml'
```

### Update `mkdocs.yml`

In your project's `mkdocs.yml`, add the shared header dropdown plugin:

```yaml
plugins:
  - search
  - header-dropdown:
      config_file: "header-dropdown.yml"
```

If your site already has a `plugins:` section, add only the
`header-dropdown` block and keep your existing plugins.

`config_file: "header-dropdown.yml"` points to the file downloaded by the CI
template at build time.

### Local Builds

For local builds only, download and commit the generated files from the root of
your documentation repository before running `mkdocs build`. With the default
`docs_dir: docs`, the logo should live in `docs/assets/`:

```bash
mkdir -p docs/assets
wget -O header-dropdown.yml \
  https://gitlab.cern.ch/cms-analysis/services/cms-docs-common/-/raw/main/data/header-dropdown.yml
wget -O docs/assets/CMSlogo_white_nolabel_1024_May2014.png \
  https://gitlab.cern.ch/cms-analysis/services/cms-docs-common/-/raw/main/CMSlogo_white_nolabel_1024_May2014.png
git add header-dropdown.yml docs/assets/CMSlogo_white_nolabel_1024_May2014.png
git commit -m "Add shared CMS docs assets for local builds"
```

GitLab CI overwrites and updates these files automatically, so this step is
only needed for local builds.

## Customization

You can extend the shared configuration with repository-specific dropdowns:

```yaml
plugins:
  - header-dropdown:
      config_file: "header-dropdown.yml"
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

To update the shared configuration used by the CI template, edit
`data/header-dropdown.yml` and/or `pog-docs.yml` in this repository and commit.
GitLab builds download the current files automatically; local-build copies can
be refreshed by rerunning the `wget` commands above.
