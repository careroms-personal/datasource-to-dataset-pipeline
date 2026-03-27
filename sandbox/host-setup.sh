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
