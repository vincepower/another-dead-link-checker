# another-dead-link-checker

This will parse a web page and validate all href references on the page.

## Using it

### Create virtual environment
```
python3 -m venv adlc
source adlc/bin/activate
```

### Loading requirements
```
python adlc.py <url>
```

## Sample output

### All good
```
python adlc https://gifted-tesla-ec935f.netlify.app/good.html
```

### Some bad
```
python adlc https://gifted-tesla-ec935f.netlify.app/bad.html
```

### All external with some redirects
```
python adlc https://gifted-tesla-ec935f.netlify.app/random.html
```
