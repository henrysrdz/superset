#!/usr/bin/env bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

# Directory where we'll unpack and run the installer
INSTALLER_DIR="/tmp/sqlanywhere_install"
mkdir -p "$INSTALLER_DIR"

# Check if a local installer file was copied to /tmp/sqlanywhere
LOCAL_INSTALLER=$(find /tmp/sqlanywhere -maxdepth 1 -name "sqla*" -type f | head -n 1)

if [ -n "$LOCAL_INSTALLER" ]; then
    echo "Found local SQL Anywhere installer: $LOCAL_INSTALLER"
    tar -xzf "$LOCAL_INSTALLER" -C "$INSTALLER_DIR"
elif [ -n "$SQLANY_INSTALLER_URL" ]; then
    echo "Downloading SQL Anywhere installer from $SQLANY_INSTALLER_URL..."
    curl -L "$SQLANY_INSTALLER_URL" -o /tmp/sqlanywhere_installer.tar.gz
    tar -xzf /tmp/sqlanywhere_installer.tar.gz -C "$INSTALLER_DIR"
    rm /tmp/sqlanywhere_installer.tar.gz
else
    echo "WARNING: No local SQL Anywhere installer (sqla*.tar.gz) or SQLANY_INSTALLER_URL was provided."
    echo "Skipping SQL Anywhere Client installation. Only database drivers will be installed."
    rm -rf "$INSTALLER_DIR"
    exit 0
fi

# Locate the setup script inside the extracted files
SETUP_SCRIPT=$(find "$INSTALLER_DIR" -name "setup" -type f | head -n 1)
if [ -z "$SETUP_SCRIPT" ]; then
    echo "ERROR: Could not find 'setup' script in the extracted installer."
    rm -rf "$INSTALLER_DIR"
    exit 1
fi

echo "Found setup script at: $SETUP_SCRIPT"
echo "Starting silent SAP SQL Anywhere client installation..."
cd "$(dirname "$SETUP_SCRIPT")"

# Execute the installer silently accepting the license
./setup -silent -nogui -I_accept_the_license_agreement || {
    echo "WARNING: Setup returned a non-zero exit status ($?), checking if libraries were installed anyway."
}

# Clean up installer files
rm -rf "$INSTALLER_DIR"

# Find where SQL Anywhere was installed (typically under /opt/sqlanywhere<version> or /opt/SAP/sqlanywhere<version>)
SQLANY_DIR=$(find /opt -maxdepth 2 -name "sqlanywhere*" -type d | head -n 1)
if [ -n "$SQLANY_DIR" ]; then
    echo "SQL Anywhere client successfully installed at $SQLANY_DIR"
    echo "Creating standardized symlink /opt/sqlanywhere -> $SQLANY_DIR..."
    ln -sf "$SQLANY_DIR" /opt/sqlanywhere
else
    echo "ERROR: Could not find SQL Anywhere installation under /opt."
    exit 1
fi
