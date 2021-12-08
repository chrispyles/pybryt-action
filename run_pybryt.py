import argparse
import base64
import dill
import json
import os
import pybryt
import tempfile
import urllib


PARSER = argparse.ArgumentParser()
PARSER.add_argument("--additional-files")
PARSER.add_argument("--ref-urls")
PARSER.add_argument("--subm")


def parse_list_arg(ref_urls):
    return [u.strip() for u in ref_urls.split("\n") if u.strip()]


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
    addl_filenames = [os.path.abspath(f) for f in parse_list_arg(args.additional_files)]

    refs = []
    for ref_url in ref_urls:
        with tempfile.NamedTemporaryFile(suffix=".pkl") as ref_ntf:
            download_url(ref_url, ref_ntf.name)
            refs.append(pybryt.ReferenceImplementation.load(ref_ntf.name))

    print("Found refs: ", ", ".join(r.name for r in refs))

    subm_path = get_full_path(args.subm)
    print("Grading ", subm_path)

    stu = pybryt.StudentImplementation(subm_path, addl_filenames=addl_filenames)
    res = stu.check(refs)
    print(pybryt.generate_report(res))

    _, json_path = tempfile.mkstemp(suffix=".json")
    print(f"::set-output name=output-json-path::{json_path}")

    with open(json_path, "w") as f:
        json.dump({
            "results": base64.b64encode(dill.dumps(res)).decode("utf-8"),
            "student_implementation": stu.dumps(),
        }, f)
    # json_str = json.dumps({
    #         "results": base64.b64encode(dill.dumps(res)).decode("utf-8"),
    #         "student_implementation": stu.dumps(),
    #     })

    # print(f"::set-output name=output-json-path::'{json_str}'")
    # with open(os.environ["GITHUB_ENV"], "a") as f:
    #     f.write(f"PYBRYT_RESULTS_JSON<<EOF\n{json_str}\nEOF\n")


if __name__ == "__main__":
    main()
