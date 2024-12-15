# Step 1: Use the official Python base image
FROM python:3.10-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy the requirements.txt into the container
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Step 5: Copy the FastAPI application code into the container
COPY . .

# Step 6: Expose the port FastAPI will run on
EXPOSE 8080

# Step 7: Set the command to run the FastAPI app using Uvicorn (ASGI server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
