FROM apache/airflow:latest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#The RUN instruction in a Dockerfile executes commands inside the container during the image build process. 
#It allows you to install software, configure the environment, or perform tasks like downloading dependencies.