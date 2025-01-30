# Copyright (C) 2016 Igalia S.L. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import re
from subprocess import check_output

from webkitpy.benchmark_runner.browser_driver.linux_browser_driver import LinuxBrowserDriver


class LinuxChromeDriver(LinuxBrowserDriver):
    browser_name = 'chrome'
    process_search_list = ['chromium', 'chromium-browser', 'chrome', 'google-chrome']

    def prepare_env(self, config):
        super().prepare_env(config)
        self._default_browser_arguments = ['--start-maximized', '--disable-extensions', '--no-first-run', '--no-default-browser-check']

    def launch_url(self, url, options, browser_build_path, browser_path):
        self._default_browser_arguments += ['--homepage', url]
        super().launch_url(url, options, browser_build_path, browser_path)

    def launch_driver(self, url, options, browser_build_path):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        for option_switch in self._default_browser_arguments:
            options.add_argument(option_switch)
        if browser_build_path:
            binary_path = os.path.join(browser_build_path, 'chromium-browser')
            options.binary_location = binary_path
        driver_executable = self.webdriver_binary_path
        driver = webdriver.Chrome(chrome_options=options, executable_path=driver_executable)
        super().launch_webdriver(url, driver)
        return driver

    def browser_version(self):
        version_cmd = [self.process_name, '--version']
        version_output = check_output(version_cmd, timeout=3).decode('utf-8', errors='ignore').strip()
        m = re.match(r'([a-zA-Z ]*)(Chrome|Chromium)([a-zA-Z ]+)([0-9.]+)', version_output)
        if m:
            return m.groups()[-1]
        version_cmd = ' '.join(version_cmd)
        raise ValueError(f'Unable to parse browser version. Command "{version_cmd}" returned "{version_output}"')
