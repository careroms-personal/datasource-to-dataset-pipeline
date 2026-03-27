#!/bin/bash
set -e

# Apply inotify limits for kind multi-node clusters
echo "Applying inotify limits for kind..."
sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl fs.inotify.max_user_instances=512
echo "Inotify limits applied."

# Persist limits across reboots
echo "Persisting inotify limits to /etc/sysctl.conf..."
if ! grep -q "fs.inotify.max_user_watches" /etc/sysctl.conf; then
  echo "fs.inotify.max_user_watches = 524288" | sudo tee -a /etc/sysctl.conf
fi
if ! grep -q "fs.inotify.max_user_instances" /etc/sysctl.conf; then
  echo "fs.inotify.max_user_instances = 512" | sudo tee -a /etc/sysctl.conf
fi
echo "Inotify limits will auto-apply on each system start."

# Install Telepresence CLI
echo "Installing Telepresence CLI..."
if command -v telepresence &> /dev/null; then
  echo "Telepresence already installed: $(telepresence version)"
else
  curl -fL https://app.getambassador.io/download/tel2/linux/amd64/latest/telepresence -o /tmp/telepresence
  chmod +x /tmp/telepresence
  sudo mv /tmp/telepresence /usr/local/bin/telepresence
  echo "Telepresence CLI installed: $(telepresence version)"
fi
