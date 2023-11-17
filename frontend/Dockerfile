# Runtime node.js 14
FROM node:14

# Working dir
WORKDIR /app

# Copy package.json and package-lock.json 
COPY package*.json ./

# Install dependencies
RUN npm install

# Copying all files
COPY . .

# Port
EXPOSE 8000

# Start 
CMD ["npm", "start"]
