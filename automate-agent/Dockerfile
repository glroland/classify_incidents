FROM registry.access.redhat.com/ubi9/python-312:9.6-1758514557

# Configuration
ENV SERVER_ADDRESS = "0.0.0.0"
ENV SERVER_PORT = "8080"
ENV OPENAI_BASE_URL = "http://localhost:11434/v1"
ENV OPENAI_API_KEY = "not_provided"
ENV PLANNING_MODEL = "openai/gpt-5"
ENV JUDGE_PLAN_MODEL = "claude/sonnet"
ENV CODING_MODEL = "claude/sonnet"
ENV WORK_DIR = "/tmp"

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
CMD [ "python", "app.py" ]
