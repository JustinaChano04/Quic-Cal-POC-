# Use slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /date_server

# Avoid tzdata timezone selection prompt
ENV DEBIAN_FRONTEND=noninteractive

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r /date_server/requirements.txt

# Copy the rest of the FastMCP app code
COPY . .

# Expose the port the FastMCP server will run on
EXPOSE 4201

# Run the server
CMD ["python", "date.py"]
