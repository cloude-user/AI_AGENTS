# Start from AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Update system packages and pip
RUN yum update -y && \
    pip install --upgrade pip setuptools wheel

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies in stages to handle conflicts better
RUN pip install --no-cache-dir \
    google-auth==2.23.4 \
    google-auth-httplib2==0.1.1 \
    google-auth-oauthlib==1.1.0

RUN pip install --no-cache-dir \
    google-api-python-client==2.108.0

RUN pip install --no-cache-dir \
    requests==2.31.0 \
    httpx==0.25.2

RUN pip install --no-cache-dir \
    pydantic==2.5.3 \
    typing-extensions==4.8.0

RUN pip install --no-cache-dir \
    openai==1.12.0

RUN pip install --no-cache-dir \
    langchain-core==0.2.28

RUN pip install --no-cache-dir \
    langchain==0.2.12

RUN pip install --no-cache-dir \
    langgraph==0.0.43

RUN pip install --no-cache-dir \
    boto3==1.34.34

# Copy all source code
COPY . .

# Verify installations
RUN python -c "import google.auth; import openai; import langchain; print('All imports successful')"

# Command to run Lambda
CMD ["main.lambda_handler"]