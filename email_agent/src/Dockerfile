# Start from AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into Lambda work dir
COPY . .

# Command to run Lambda
CMD ["main.lambda_handler"]
