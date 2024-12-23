# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code into the container (if applicable)
COPY . .

# Command to navigate to Dashboard/ and run dashboard.py with Streamlit
CMD ["sh", "-c", "cd Dashboard && streamlit run dashboard.py"]

# Expose the port (only needed if using Streamlit or similar)
EXPOSE 8501
