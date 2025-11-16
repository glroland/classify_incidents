FROM registry.access.redhat.com/ubi9/python-312:9.6-1758514557

# Configuration
ENV OPENAI_BASE_URL = "http://localhost:11434/v1"
ENV OPENAI_API_KEY = "not_provided"
ENV OPENAI_MODEL = "granite4"
ENV SERVICE_NOW_INSTANCE = ""
ENV SERVICE_NOW_USERNAME = ""
ENV SERVICE_NOW_PASSWORD = ""
ENV API_TIMEOUT = "60"
ENV PROMPTS_LOCATION = "./prompts/"
ENV OBJECT_STORAGE_URL = ""
ENV OBJECT_STORAGE_ACCESS_KEY = ""
ENV OBJECT_STORAGE_SECRET_KEY = ""
ENV OBJECT_STORAGE_BUCKET = ""

# By default, listen on port 8080
EXPOSE 8080/tcp

# Set the working directory in the container
WORKDIR /projects

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./src/ .

# Specify the command to run on container start
CMD ["streamlit", "run", "./app.py", "--server.port=8080", "--server.address=0.0.0.0"]
