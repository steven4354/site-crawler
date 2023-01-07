FROM python:3.8
COPY script.py /app/
RUN pip install requests bs4
WORKDIR /app
CMD ["python", "script.py"]
VOLUME /app
