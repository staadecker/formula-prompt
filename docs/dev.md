# Notes to self on how to manage this package

## Process to release new versions.

1. Bump version in `setup.cfg`.

2. Run `python -m build`. Might require running `pip install build`.

3. Run `twine upload dist/*`. Will prompt for pypi.org password. Might require running `pip install twine`.

4. Commit to Github

5. On Github, go to, Releases -> Draft New Release then set the version the publish the release.