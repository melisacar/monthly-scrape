FROM postgres:13

#The RUN instruction in a Dockerfile executes commands inside the container during the image build process. 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt