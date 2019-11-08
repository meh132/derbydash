FROM python

WORKDIR /usr/src/app

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install dash==1.4.1  # The core dash backend
RUN pip install dash-daq==0.2.1  # DAQ components (newly open-sourced!)

# Bundle app source
COPY app.py /src/app.py

EXPOSE  8050
CMD ["/bin/bash"]


# docker run -it -v ${PWD}:"/usr/src" -p 8050:8050 python /bin/bash