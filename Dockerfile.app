FROM python:3.10-slim

WORKDIR /home/app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5672
EXPOSE 8000
EXPOSE 27017

# CMD ["bash"]
CMD [ "python", "src/main.py"]
