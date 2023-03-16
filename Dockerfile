FROM python:3.9-slim-buster

RUN mkdir -p /opt/flex_visualizer
RUN mkdir -p /tmp/gtfs

COPY *.py /opt/flex_visualizer/

COPY start.sh /opt/flex_visualizer/

RUN chmod +x /opt/flex_visualizer/start.sh

COPY requirements.txt /opt/flex_visualizer/

RUN pip install -r /opt/flex_visualizer/requirements.txt


ENTRYPOINT ["/opt/flex_visualizer/start.sh"]