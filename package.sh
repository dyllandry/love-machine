#!/bin/bash

# Setup dist directory
rm -r dist
mkdir -p dist

# Install dependencies
pip3 install --target dist/vendor -r requirements.txt

# # Zip dependencies
cd dist/vendor
pwd
zip -r ../deployment-package.zip ./
cd -
pwd

# Clean up dependencies
rm -r dist/vendor

# Zip app
cd app
pwd
# Quote exclude path to avoid bash filename expansion prior to zip parsing it.
zip -gr ../dist/deployment-package.zip ./ --exclude "__pycache__/*"
cd -
pwd
