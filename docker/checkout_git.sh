
# use https urls as a temporary measure, should just set up an access key
git config --global url."https://github.com/".insteadOf git@github.com:
git config --global url."https://".insteadOf git://

# if no branch set, use master
used_branch=${BRANCH:-master}
git fetch origin "${used_branch}"
git checkout "${used_branch}"

# if specific commit given, make new branch from this commit
if [[ -n "$COMMIT_HASHCODE" ]]; then
  git checkout -b "commit_${COMMIT_HASHCODE}" "${COMMIT_HASHCODE}"
fi;
