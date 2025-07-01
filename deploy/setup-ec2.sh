#!/bin/bash

# FastAPI Service EC2 Setup Script
# Run this script on your EC2 instance to set up the environment

set -e

echo "🚀 Setting up EC2 instance for FastAPI service..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt install -y python3 python3-pip git nginx curl

# Install uv (Python package manager)
echo "📦 Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Add uv to PATH for this session
export PATH="$HOME/.local/bin:$PATH"

# Create application directory
echo "📁 Creating application directory..."
mkdir -p /home/ubuntu/fastapi-service

# Set up firewall (allow HTTP, HTTPS, SSH)
echo "🔒 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8000  # For direct FastAPI access during testing
sudo ufw --force enable

# Configure nginx
echo "🌐 Configuring nginx..."
sudo systemctl enable nginx
sudo systemctl start nginx

# Create a simple nginx test page
sudo tee /var/www/html/index.html > /dev/null <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Service - Server Ready</title>
</head>
<body>
    <h1>FastAPI Service Server Ready</h1>
    <p>Nginx is running. FastAPI service will be available after deployment.</p>
    <p>Server IP: $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)</p>
</body>
</html>
EOF

# Set up log rotation for the application
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/fastapi-service > /dev/null <<EOF
/var/log/fastapi-service.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
EOF

# Create directory for application logs
sudo mkdir -p /var/log
sudo touch /var/log/fastapi-service.log
sudo chown ubuntu:ubuntu /var/log/fastapi-service.log

echo "✅ EC2 setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add your SSH public key to ~/.ssh/authorized_keys"
echo "2. Set up GitHub secrets with:"
echo "   - EC2_HOST: $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "   - EC2_USERNAME: ubuntu"
echo "   - EC2_SSH_KEY: (your private key)"
echo "3. Push your code to GitHub to trigger deployment"
echo ""
echo "🌐 Test nginx: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
