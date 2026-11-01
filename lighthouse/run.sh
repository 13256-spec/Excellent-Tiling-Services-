#!/usr/bin/env bash
# Usage: lighthouse/run.sh <label> <url> [runs]
# Runs Lighthouse (mobile + desktop) N times each and writes lighthouse/<label>/{mobile,desktop}-<n>.json.
# Needs lighthouse on PATH (npm i -g lighthouse) or LH=path/to/lighthouse.
set -euo pipefail
label=$1; url=$2; runs=${3:-3}
LH=${LH:-lighthouse}
CHROME_PATH=${CHROME_PATH:-$(ls -d /opt/pw-browsers/chromium-*/chrome-linux64/chrome 2>/dev/null | head -1)}
export CHROME_PATH
out="$(dirname "$0")/$label"; mkdir -p "$out"
flags="--headless=new --no-sandbox --disable-gpu"
[ -n "${HTTPS_PROXY:-}" ] && flags="$flags --proxy-server=$HTTPS_PROXY"
for i in $(seq 1 "$runs"); do
  for ff in mobile desktop; do
    preset=""; [ "$ff" = desktop ] && preset="--preset=desktop"
    "$LH" "$url" $preset --quiet --output=json --output-path="$out/$ff-$i.json" \
      --chrome-flags="$flags" --only-categories=performance,accessibility,best-practices,seo || echo "run $ff-$i failed"
  done
done
