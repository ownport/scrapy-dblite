FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        python-pip 

RUN pip install nose coverage

RUN mkdir -p /data/bin
RUN mkdir -p /data/scrapy-dblite

ADD scripts/create-env.sh /data/bin/
RUN chmod +x /data/bin/*.sh

CMD /data/bin/create-env.sh
