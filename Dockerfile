# Use the official Playwright Docker image which already has all the required Linux browser dependencies!
FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

# Set the working directory
WORKDIR /app

# Copy your requirements.txt first
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the automation script
CMD ["python", "playwright_main.py"]
