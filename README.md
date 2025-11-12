# CMS Documentation Common Configuration

Shared configuration and assets for CMS documentation sites using the [mkdocs-header-dropdown-plugin](https://github.com/cms-cat/mkdocs-header-dropdown-plugin).

## Contents

- **header-dropdown.yml**: Standard CMS POG documentation dropdown configuration
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

## Maintaining

To update the shared configuration, edit `header-dropdown.yml` in this repository and commit. All documentation sites using this as a submodule can then pull the updates.
