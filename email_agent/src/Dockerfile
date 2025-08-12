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
RUN pip install --no-cache-dir -r requirements.txt
# Copy all source code
COPY . .


# Command to run Lambda
CMD ["main.lambda_handler"]