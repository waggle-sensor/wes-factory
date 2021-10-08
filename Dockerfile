FROM python:alpine3.13

# Add necessary python libraries
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .
ENTRYPOINT [ "python", "main.py" ]