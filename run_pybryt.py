import argparse
import os
import pybryt
import tempfile
import urllib

from pybryt.reference import generate_report


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--ref")
PARSER.add_argument("--subm")


def get_full_path(repo_path):
    workspace_path = os.environ["GITHUB_WORKSPACE"]
    return os.path.join(workspace_path, repo_path)


def download_url(url, save_path):
    print(url)
    url = urllib.request.urlopen(url)
    with open(save_path, "wb") as f:
        f.write(url.read())


def main():
    args = PARSER.parse_args()

    print(os.listdir(get_full_path("")))

    with tempfile.NamedTemporaryFile(suffix=".pkl") as ref_ntf:
        download_url(args.ref, ref_ntf.name)
        ref = pybryt.ReferenceImplementation.load(ref_ntf.name)

    print("Found ref: ", ref.name)

    subm_path = get_full_path(args.subm)
    print("Grading ", subm_path)

    stu = pybryt.StudentImplementation(subm_path)
    res = stu.check(ref)
    print(pybryt.generate_report(res))


if __name__ == "__main__":
    main()
