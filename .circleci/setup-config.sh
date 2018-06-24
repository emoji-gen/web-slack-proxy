#!/bin/bash

set -eu -o pipefail

git rm externals/conf
git commit -m 'fix(externals): remove private module'
