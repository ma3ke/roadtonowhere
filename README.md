# Road to Nowhere

A script to check files for broken http urls.

It finds the urls in each of the specified documents, and performs a get request for each of the urls.
It reports the exit code of the request to stdout, making it clear which and how many urls are broken.

```
usage: main.py [-h] path [path ...]

check a document for broken urls

positional arguments:
  path        a file to be checked

options:
  -h, --help  show this help message and exit
```

Currently, the script has naive support for:

- `.html` **html** (heuristic: starts with `href="http{s}://`, ends with `"`)
- `.md` **markdown** (heuristic: starts with `(http{s}://`, ends with `)`)
- other filetypes (heuristic: starts with `http{s}://`, ends with a whitespace character)

These heuristics are imperfect, but they do get the job done in most circumstances.

Created by ma3ke/Koen Westendorp, 2023. I hope you have a nice day :)
