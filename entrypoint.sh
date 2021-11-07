#!/bin/sh -l

conda run -n pybryt-env python3 /install_requirements.py
conda run -n pybryt-env python3 /run_pybryt.py "$@"
