# 1. Navigate to your BandGap-ml directory
# 2. Run the Docker build command:
    # docker build -t bandgap-ml-backend -f backend/Dockerfile .
    # This command tells Docker to:
      # Use the Dockerfile located in the backend directory (-f backend/Dockerfile)
      # Use the current directory (.) as the build context, which includes both backend and band_gap_ml directories
      # Tag the resulting image as bandgap-ml-backend
# 3. Run the container:
     #    # docker run -p 3000:3000 bandgap-ml-backend

FROM condaforge/miniforge3:latest AS bandgap-ml-backend

ENV PYTHON_VERSION=3.12

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update conda and install Python 3.12
RUN conda update -n base -c conda-forge conda && \
    conda install -y -c conda-forge python=${PYTHON_VERSION} && \
    conda clean -afy

WORKDIR /code

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install the latest version of BandGap-ml from Git
RUN pip install git+https://github.com/alexey-krasnov/BandGap-ml.git

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD ["uvicorn", "band_gap_ml.app:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "1", "--timeout-keep-alive", "3600"]