# Road to Nowhere

A script to check files for broken http urls.

It finds the urls in each of the specified documents, and performs a get request for each of the urls.
It reports the exit code of the request to stdout, making it clear which and how many urls are broken.

## Usage

```
usage: main.py [-h] path [path ...]

check a document for broken urls

positional arguments:
  path        a file to be checked

options:
  -h, --help  show this help message and exit
```

### Example

To check the files in the _examples_ directory, run

```console
$ roadtonowhere examples/*
```

And the output will look something like this:

```
Parsing 'examples/example.html'... found 1 urls. Checking for broken urls...
        ok: [200] https://www.iana.org/domains/example
Found 0 broken urls in 'examples/example.html'.

Parsing 'examples/example.md'... found 5 urls. Checking for broken urls...
        ok: [200] https://hachyderm.io/@ma3ke
    BROKEN: [404] https://example.com/this_page_does_not_exist.html
        ok: [200] https://dwangschematiek.nl/
        ok: [200] https://twitter.com/
    BROKEN: [404] http://example.com/some_more_requests_to_non-existent_pages.html
Found 2 broken urls in 'examples/example.md'.
```

## Filetypes

Currently, the script has naive support for:

- `.html` **html** (heuristic: starts with `href="http{s}://`, ends with `"`)
- `.md` **markdown** (heuristic: starts with `(http{s}://`, ends with `)`)
- other filetypes (heuristic: starts with `http{s}://`, ends with a whitespace character)

These heuristics are imperfect, but they do get the job done in most circumstances.

Created by ma3ke/Koen Westendorp, 2023. I hope you have a nice day :)
