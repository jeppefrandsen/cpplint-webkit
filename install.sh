#!/bin/sh

sudo cp -r cpplint-webkit/WebKit /usr/share
sudo cp cpplint-webkit/check-webkit-style /usr/bin
sudo cp cpplint-webkit/cpplint-webkit /usr/bin
sudo git init /usr/share/WebKit
sudo git config --global --add safe.directory /usr/share/WebKit
