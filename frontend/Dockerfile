# To build and run this Docker image:
# 1. Build the image:
    # docker build -t bandgap-ml-frontend -f frontend/Dockerfile .

#2. Run the container:
    # docker run -p 8080:8080 bandgap-ml-frontend

# Use an official Node runtime as the base image
FROM node:22

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Install Vue CLI globally
RUN npm install -g @vue/cli

# Copy the rest of the frontend code
COPY frontend/ .

# Install project dependencies
RUN npm install

# Build the app for production
RUN npm run build

# Install serve to run the production build
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 8080

# Serve the production build
CMD ["serve", "-s", "dist", "-l", "8080"]