#!/bin/bash

set -eu -o pipefail

git config --global user.email 'ultimate.emoji.gen@gmail.com'
git config --global user.name 'Emoji Generator'

# Copy app config
cp externals/conf/app/web-slack-proxy.yml config/production.yml
git add config/production.yml
git commit -m 'fix(config): add production conf'

# Remove private submodule
git rm externals/conf
git commit -m 'fix(externals): remove private module'

