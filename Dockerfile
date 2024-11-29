FROM apache/airflow:latest

# UTF-8 settings.
ENV PYTHONUTF8=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#The RUN instruction in a Dockerfile executes commands inside the container during the image build process. 
#It allows you to install software, configure the environment, or perform tasks like downloading dependencies.