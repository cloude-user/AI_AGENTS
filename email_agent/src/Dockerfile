# Start from AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Set workdir to Lambda's default
WORKDIR /var/task

# Set PYTHONPATH to /var/task for absolute imports
ENV PYTHONPATH=/var/task

# Copy requirements and install dependencies
COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into Lambda work dir
COPY src/ .

# Command to run Lambda
CMD ["main.lambda_handler"]
