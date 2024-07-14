#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static
# Check if Nginx is installed
if ! command -v nginx &>/dev/null; then
    echo "Nginx is not installed. Installing Nginx..."
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo ufw allow 'Nginx HTTP'

# Create the necessary directories
if [ ! -d "/data" ]; then
    sudo mkdir -p /data/web_static{/releases/test,/shared}
fi

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    <h1>Hello Holberton!</h1>
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create/update the symbolic link
if [ -L "/data/web_static/current" ]; then
    sudo rm "/data/web_static/current"
fi
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of the /data/ folder
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
sudo tee /etc/nginx/sites-available/default >/dev/null <<EOF
OF
server {
    listen 80;
    listen [::]:80 default_server;
    root   /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
    add_header X-Served-By \$HOSTNAME;
    location /hbnb_static {
        alias /data/web_static/current;
    }
}
EOF

# Restart Nginx
sudo service nginx restart
