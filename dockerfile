FROM python

#WORKDIR /usr/src

# Update
#RUN apk add --update python py-pip

# Install app dependencies
RUN pip install dash==1.4.1  # The core dash backend
RUN pip install dash-daq==0.2.1  # DAQ components (newly open-sourced!)
RUN pip install pandas
RUN pip install pyserial

# Bundle app source
#COPY app.py /src/app.py

EXPOSE  8050
CMD ["/bin/bash"]



pip install dash==1.4.1  # The core dash backend
pip install dash-daq==0.2.1  # DAQ components (newly open-sourced!)
pip install pandas
pip install pyserial
# docker run -it -v ${PWD}:"/usr/src" -p 8050:8050 python /bin/bash
