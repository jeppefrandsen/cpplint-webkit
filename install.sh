#!/bin/sh

sudo cp -r WebKit /usr/share
sudo cp check-webkit-style /usr/bin
sudo cp cpplint /usr/local/bin
sudo git init /usr/share/WebKit
sudo git config --global --add safe.directory /usr/share/WebKit
