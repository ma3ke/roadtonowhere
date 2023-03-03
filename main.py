import argparse
import requests

TIMEOUT_SECONDS = 10


def report_timeout(url: str) -> str:
    return f"   timeout: request took more than {TIMEOUT_SECONDS} seconds {url}"


def report_ok(url: str, code: int) -> str:
    return f"        ok: [{code:03}] {url}"


def report_broken(url: str, code: int) -> str:
    return f"    BROKEN: [{code:03}] {url}"


def report(url: str, status: int | None) -> int:
    broken = 0
    match status:
        case None:
            print(report_timeout(url))
        case 200:
            print(report_ok(url, status))
        case err_code:
            broken += 1
            print(report_broken(url, err_code))
    return broken


def report_all(results: list[tuple[str, int]]):
    for url, status in results:
        report(url, status)


def check(url: str) -> int | None:
    try:
        return requests.get(url, timeout=TIMEOUT_SECONDS).status_code
    except KeyboardInterrupt:
        exit(1)
    except requests.Timeout:
        return None


def parse_urls(path: str, filetype: None | str = None) -> list[str] | None:
    if filetype == None:
        _, filetype = path.rsplit(".")

    with open(path, "r") as file:
        contents = file.read()

    # Specify the heuristic for finding the start of a url depending on the
    # filetype.
    match filetype:
        case "html":
            http_heuristic = 'href="http://'
            https_heuristic = 'href="https://'
        case "md":
            http_heuristic = "(http://"
            https_heuristic = "(https://"
        case _:
            http_heuristic = "http://"
            https_heuristic = "https://"

    n_urls = contents.count(http_heuristic) + contents.count(https_heuristic)
    if n_urls == 0:
        return None

    indices = []
    start = 0
    while True:
        # Look for both http and https schemes.
        http_index = contents.find(http_heuristic, start)
        https_index = contents.find(https_heuristic, start)
        match http_index, https_index:
            case -1, -1:
                # No start of the url for either scheme was found.
                break
            case p, -1:
                # Found an http:// somewhere.
                offset = p
            case -1, s:
                # Found an https:// somewhere.
                offset = s
            case p, s:
                # Found both http:// and https://. We take a look at the
                # closest one. We will get to the other one eventually.
                offset = min(p, s)
        indices.append(offset)
        start = offset + 1

    # Specify the heuristic for finding the end of a url depending on the
    # filetype.
    match filetype:
        case "html":
            end_condition = lambda c: c == '"'
        case "md":
            end_condition = lambda c: c == ")"
        case _:
            end_condition = lambda c: c.isspace()

    urls = []
    for start in indices:
        remainder = contents[start:]
        # Skip the possible 'href="' or '(' before the scheme.
        start = len(http_heuristic) - len("http://")
        end = start
        # Scan the whole remainder until a whitespace or the end of file
        # has been reached.
        while end < len(remainder) and not end_condition(remainder[end]):
            end += 1
        url = remainder[start:end]
        urls.append(url)

    return urls


def check_paths(paths: list[str]):
    for path in paths:
        print(f"Parsing '{path}'...", end=" ")
        urls = parse_urls(path)
        if urls == None:
            print("no urls found.")
            break
        print(f"found {len(urls)} urls.", end=" ")

        print(f"Checking for broken urls...")
        broken = 0
        for url in urls:
            status = check(url)
            broken += report(url, status)
        print(f"Found {broken} broken urls in '{path}'.\n")


def main():
    parser = argparse.ArgumentParser(
        description="check a document for broken urls",
        epilog="By ma3ke, 2023. I hope you have a nice day :)",
    )
    parser.add_argument(
        "documents", metavar="path", nargs="+", type=str, help="a file to be checked"
    )
    args = parser.parse_args()

    paths = args.documents
    check_paths(paths)


if __name__ == "__main__":
    main()
