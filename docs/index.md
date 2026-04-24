# GitLab CI Template

Use this repository's GitLab CI template to build and publish an MkDocs site
with the shared CMS setup.

## Include it

In your project's `.gitlab-ci.yml`, add:

```yaml
include:
  - project: 'cms-analysis/services/cms-docs-common'
    file: 'mkdocs-gitlab-pages.gitlab-ci.yml'
```

## Update `mkdocs.yml`

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

## Local Builds

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

## What it does

- Uses `ghcr.io/cms-cat/mkdocs-material:latest` as the build image.
- Installs `requirements.txt` if your project provides one.
- Checks out git submodules recursively.
- Downloads the shared `header-dropdown.yml`.
- Downloads the CMS logo asset into `assets/` inside your MkDocs `docs_dir` using the value defined in your `mkdocs.yml`.
- Runs `mkdocs build -d public`.
- Runs a `validation` job on non-default branches.
- Runs a `pages` job on the default branch and publishes `public/`.

The template itself lives in `mkdocs-gitlab-pages.gitlab-ci.yml`.
