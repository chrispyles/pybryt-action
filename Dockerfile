FROM ubuntu:18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget -nv -O /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash /tmp/miniconda.sh -b
RUN conda --version

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

ADD install_requirements.py /install_requirements.py
ADD run_pybryt.py /run_pybryt.py
ADD entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
