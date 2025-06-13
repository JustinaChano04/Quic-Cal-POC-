FROM python:3.11-slim

# Set working directory
WORKDIR /gcal_server


# Set environment variable to avoid tzdata interactive prompt
ENV DEBIAN_FRONTEND=noninteractive

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r /gcal_server/requirements.txt

# Copy your app code
COPY . .

# Expose FastMCP server port
EXPOSE 4200

# Launch FastMCP server
CMD ["python", "gcal.py"]
