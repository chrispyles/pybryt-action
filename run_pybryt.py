import argparse
import os
import pybryt
import tempfile
import urllib


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--ref")
PARSER.add_argument("files", nargs=-1)


def download_url(url, save_path):
    url = urllib.urlopen(url)
    with open(save_path, "wb") as f:
        f.write(url.read())


def main():
    args = PARSER.parse_args()

    print(os.listdir(os.environ["GITHUB_WORKSPACE"]))

    with tempfile.NamedTemporaryFile(suffix=".pkl") as ref_ntf:
        download_url(args.ref, ref_ntf.name)
        ref = pybryt.ReferenceImplementation.load(ref_ntf.name)

    print("Found ref: ", ref)

    for file in args.files:
        print("Grading ", file)


if __name__ == "__main__":
    main()