FROM python:3.8.0-buster

# Make a directory for our application
RUN mkdir /bravo2api
WORKDIR /bravo2api

# Install Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy Source Code 
COPY . .

# Run App
CMD ["python", "app.py"]
