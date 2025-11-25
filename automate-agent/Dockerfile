FROM registry.access.redhat.com/ubi9/python-312:9.6-1758514557

# Configuration
ENV SERVER_ADDRESS = "0.0.0.0"
ENV SERVER_PORT = "8080"
ENV NUM_WORKERS = "0"
ENV LOG_LEVEL = "info"
ENV OPENAI_BASE_URL = "http://localhost:11434/v1"
ENV OPENAI_API_KEY = "not_provided"
ENV PLANNING_MODEL = "openai/gpt-5"
ENV JUDGE_PLAN_MODEL = "canthropic/claude-3-7-sonnet-20250219"
ENV CODING_MODEL = "anthropic/claude-3-7-sonnet-20250219"
ENV WORK_DIR = "/tmp"

USER root

# Install ShellCheck
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
    dnf install -y shellcheck && \
    dnf clean all

# Install Powershell via RPM package from microsoft repo
RUN curl -sSL -O https://packages.microsoft.com/config/rhel/9/packages-microsoft-prod.rpm && \
    rpm -i packages-microsoft-prod.rpm && \
    rm packages-microsoft-prod.rpm && \
    dnf install powershell -y

USER 1001

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
