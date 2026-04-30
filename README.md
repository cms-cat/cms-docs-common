# CMS Documentation Common Configuration

Shared configuration and assets for CMS documentation sites using the [mkdocs-header-dropdown-plugin](https://github.com/cms-cat/mkdocs-header-dropdown-plugin).

## Contents

- **header-dropdown.yml**: Committed dropdown bootstrap configuration.
- **pog-docs.yml**: Authoritative dropdown link data refreshed by CI.
- **CMSlogo_white_nolabel_1024_May2014.png**: CMS logo for the header dropdown.
- **mkdocs-gitlab-pages.gitlab-ci.yml**: Shared GitLab CI template for MkDocs builds.

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

### Add the Committed Shared Files

Download and commit the shared files from the root of your documentation
repository. With the default `docs_dir: docs`, the logo should live in
`docs/assets/`:

```bash
mkdir -p docs/assets
wget -O header-dropdown.yml \
  https://gitlab.cern.ch/cms-analysis/services/cms-docs-common/-/raw/main/header-dropdown.yml
wget -O pog-docs.yml \
  https://gitlab.cern.ch/cms-analysis/services/cms-docs-common/-/raw/main/pog-docs.yml
wget -O docs/assets/CMSlogo_white_nolabel_1024_May2014.png \
  https://gitlab.cern.ch/cms-analysis/services/cms-docs-common/-/raw/main/CMSlogo_white_nolabel_1024_May2014.png
git add header-dropdown.yml pog-docs.yml docs/assets/CMSlogo_white_nolabel_1024_May2014.png
git commit -m "Add shared CMS docs dropdown files"
```

The CI template refreshes only `pog-docs.yml` at build time, because that is
the file expected to change when shared links are updated. Keep
`header-dropdown.yml` and the CMS logo committed in each documentation
repository. Rerun the commands above only if the bootstrap config or logo
changes.

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

## Link Data

The shared `header-dropdown.yml` uses `auto_generate_from` to build the CMS Docs
dropdown from `pog-docs.yml`.

To add or update shared links, edit `pog-docs.yml` in this repository:

```yaml
pog_docs:
  "Top-level Link":
    fallback: "https://example.com"
    border-bottom: true

  "Menu Group":
    "Child Link": "https://example.com/child"
```

The plugin recognizes `fallback` or `url` as the clickable parent URL, and
passes link metadata such as `target` and `border-bottom` through to generated
parent links. Other string values become submenu links.

More info: https://cms-analysis-corrections.docs.cern.ch/development/

## What the CI Template Does

- Uses `ghcr.io/cms-cat/mkdocs-material:latest` as the build image.
- Installs `requirements.txt` if your project provides one.
- Checks out git submodules recursively.
- Downloads the current shared `pog-docs.yml`.
- Uses the committed `header-dropdown.yml` and CMS logo from your repository.
- Runs `mkdocs build -d public`.
- Runs a `validation` job on non-default branches.
- Runs a `pages` job on the default branch and publishes `public/`.

The template itself lives in `mkdocs-gitlab-pages.gitlab-ci.yml`.

## Maintaining

When updating these instructions, keep `README.md` and `docs/index.md` in sync.
