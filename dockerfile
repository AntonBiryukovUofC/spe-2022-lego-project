FROM rocker/tidyverse:4.2
#RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base=${R_BASE_VERSION} r-base-dev=${R_BASE_VERSION}  \
#    && rm -rf /var/lib/apt/lists/*
#RUN /bin/sh -c apt-get update && apt-get install -y --no-install-recommends libopenblas0-pthread littler r-cran-docopt r-cran-littler r-base=${R_BASE_VERSION}-* r-base-dev=${R_BASE_VERSION}-* r-base-core=${R_BASE_VERSION}-* r-recommended=${R_BASE_VERSION}-* && ln -s /usr/lib/R/site-library/littler/examples/install.r /usr/local/bin/install.r && ln -s /usr/lib/R/site-library/littler/examples/install2.r /usr/local/bin/install2.r && ln -s /usr/lib/R/site-library/littler/examples/installBioc.r /usr/local/bin/installBioc.r && ln -s /usr/lib/R/site-library/littler/examples/installDeps.r /usr/local/bin/installDeps.r && ln -s /usr/lib/R/site-library/littler/examples/installGithub.r /usr/local/bin/installGithub.r && ln -s /usr/lib/R/site-library/littler/examples/testInstalled.r /usr/local/bin/testInstalled.r && rm -rf /tmp/downloaded_packages/ /tmp/*.rds 	&& rm -rf /var/lib/apt/lists/*
RUN R -e "install.packages('rjson',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('png',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('remotes',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e 'remotes::install_github("ryantimpe/brickr")'
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev python3.9 python3-pip python3-setuptools python3-dev
RUN pip3 install --upgrade pip
# here i assume that python and R scripts are in the same directory
# create packages with versions into requirements.txt
# how to create?
COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt
COPY Legofy.py /opt/src/Legofy.py
Copy RCode_brickr.R /opt/src/RCode_brickr.R
EXPOSE 8600
WORKDIR opt/src
ENTRYPOINT ["streamlit", "run","--server.port","8600","Legofy.py"]