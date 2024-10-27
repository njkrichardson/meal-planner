# syntax=docker/dockerfile:1

FROM ubuntu:22.04 
LABEL maintainer="njkrichardson@gmail.com" 

WORKDIR /meal_planner
ENV PYTHONPATH=/meal_planner:/meal_planner/src

COPY ./build/requirements.txt /requirements.txt

# ubuntu dependencies 
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --yes \
    build-essential \
    curl \
    git \ 
    python3-pip


# install python dependencies 
RUN pip install -r /requirements.txt

CMD ["/bin/bash"]
