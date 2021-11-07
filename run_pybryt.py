import argparse
import os
import pybryt
import tempfile
import urllib


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--ref-urls")
PARSER.add_argument("--subm")


def parse_list_arg(ref_urls):
    return [u.strip for u in ref_urls.split("\n")]


def get_full_path(repo_path):
    workspace_path = os.environ["GITHUB_WORKSPACE"]
    return os.path.join(workspace_path, repo_path)


def download_url(url, save_path):
    url = urllib.request.urlopen(url)
    with open(save_path, "wb") as f:
        f.write(url.read())


def main():
    args = PARSER.parse_args()

    print(os.listdir(get_full_path("")))

    ref_urls = parse_list_arg(args.ref_urls)

    refs = []
    for ref_url in ref_urls:
        with tempfile.NamedTemporaryFile(suffix=".pkl") as ref_ntf:
            download_url(ref_url, ref_ntf.name)
            refs.append(pybryt.ReferenceImplementation.load(ref_ntf.name))

    print("Found refs: ", ", ".join(r.name for r in refs))

    subm_path = get_full_path(args.subm)
    print("Grading ", subm_path)

    stu = pybryt.StudentImplementation(subm_path)
    res = stu.check(refs)
    print(pybryt.generate_report(res))


if __name__ == "__main__":
    main()
