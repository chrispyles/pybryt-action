import os
import subprocess


ENV_NAME = "pybryt-env"


def main():
    reqs_path = os.path.join(os.environ["GITHUB_WORKSPACE"], "requirements.txt")
    if os.path.isfile(reqs_path):
        subprocess.run(["conda", "run", "-n", ENV_NAME, "pip", "install", "-r", reqs_path])


if __name__ == "__main__":
    main()
