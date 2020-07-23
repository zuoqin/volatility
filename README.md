[![Build Status](https://travis-ci.org/zuoqin/volatility.svg)](https://travis-ci.org/zuoqin/volatility)
[![Maintainability](https://api.codeclimate.com/v1/badges/45932400a1661926a3ba/maintainability)](https://codeclimate.com/github/zuoqin/volatility/maintainability)
[![Hits-of-Code](https://hitsofcode.com/github/zuoqin/volatility)](https://hitsofcode.com/github/zuoqin/volatility)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/zuoqin/takes/blob/master/LICENSE.txt)


### Build
```
python3 setup.py sdist bdist_wheel
```

### Upload package
```
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Next, calculate the volatility, using `volatility` command.
For a Git repository:

```
$ volatility --path .
```
Volatility will be output in percentages.

That's it.
