# Manual EC2 Setup Commands

If you prefer to run commands manually instead of downloading the script, here are all the commands:

## Step 1: Install curl (if not available)
```bash
sudo apt install -y curl
```

## Step 2: Install required packages
```bash
sudo apt install -y python3 python3-pip git nginx
```

## Step 3: Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

## Step 4: Create application directory
```bash
mkdir -p /home/ubuntu/fastapi-service
```

## Step 5: Configure firewall
```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw allow 8000
sudo ufw --force enable
```

## Step 6: Start nginx
```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

## Step 7: Create test page
```bash
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
```

## Step 8: Set up logging
```bash
sudo mkdir -p /var/log
sudo touch /var/log/fastapi-service.log
sudo chown ubuntu:ubuntu /var/log/fastapi-service.log
```

## Step 9: Get your server IP
```bash
curl -s http://169.254.169.254/latest/meta-data/public-ipv4
```

Use this IP for your GitHub secrets configuration.
