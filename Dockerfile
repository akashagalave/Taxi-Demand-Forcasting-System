FROM python:3.12.7

WORKDIR /app/

COPY requirements-docker.txt .

# Install Python dependencies and DVC
RUN pip install --upgrade pip && pip install -r requirements-docker.txt

# Copy the entire project including DVC data (already pulled in CI/CD)
COPY . .

# Expose port and run Streamlit
EXPOSE 8000

CMD ["streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
