#!/bin/bash

set -eu -o pipefail

git config --global user.email 'ultimate.emoji.gen@gmail.com'
git config --global user.name 'Emoji Generator'

# Remove private submodule
git rm externals/conf
git commit -m 'fix(externals): remove private module'

