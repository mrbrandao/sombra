# Publishing the docs site

The vitepress site is deployed automatically to
<https://mrbrandao.github.io/sombra/> by the
[`docs.yml`](https://github.com/mrbrandao/sombra/blob/main/.github/workflows/docs.yml)
workflow. Any push to `main` touching `docs/`, `package.json`,
`package-lock.json`, `README.md`, or the workflow itself triggers a rebuild and
deploy. A manual run is always available via **Actions → Docs →
Run workflow**.

## One-time bootstrap

Before the first deploy, GitHub Pages must be enabled with the **GitHub
Actions** source. This is already done for this repo, but a fresh fork or
rename must repeat it:

1. **Settings → Pages → Source: GitHub Actions**, or
2. via the API:

   ```bash
   gh api repos/<owner>/<repo>/pages -X POST -f build_type=workflow
   ```

Until this is done, `deploy-pages` fails with `Not Found` and the message
"Ensure GitHub Pages has been enabled".

## Troubleshooting

### `Multiple artifacts named "github-pages"` on deploy

`deploy-pages` refuses to run when a run carries more than one
`github-pages` artifact. This happens when you rerun only the failed deploy
job — the retry uploads a fresh artifact while the one from the original run
is still on record.

**Fix:** rerun the **whole** workflow run, not a single job:

```bash
gh run rerun <run-id>          # full run, single artifact
```

or trigger a fresh `workflow_dispatch` run. Each full run uploads exactly one
artifact, keeping the count at 1:1.

### Node 20 deprecation warnings

The pinned actions may warn that they target Node 20 and are forced onto
Node 24. This is non-blocking — the pipeline still deploys.

## Updating pinned actions

The four actions in `docs.yml` are pinned to commit SHAs for supply-chain
stability. To bump one to the latest release:

```bash
gh api repos/actions/deploy-pages/git/ref/tags/v4 --jq '.object.sha'
```

Update the SHA in the workflow and keep the trailing `# vN` tag comment as
the human-readable version marker.