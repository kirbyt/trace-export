#!/usr/bin/python
#
# trace-export.py
#
# Copyright (c) 2016 Kirby Turner
#
# Version 1.0.0
#
# This script downloads the GPX data from a Trace user's account.
#
# Usage: python trace-export.py your@email.com your-password
#
# Written for Python 2.7.x. Requires BeautifulSoup available at:
# https://www.crummy.com/software/BeautifulSoup/
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#


import urllib
import urllib2
import cookielib
import sys
from bs4 import BeautifulSoup


def requestHtml(opener, url, data=None):
    request = urllib2.Request(url, data)
    urlHandle = opener.open(request)
    html = urlHandle.read()
    return html


def scrapeIt():
    handlers = []
    cj = cookielib.CookieJar();
    cj.set_policy(cookielib.DefaultCookiePolicy(rfc2965=True))
    cjhdr = urllib2.HTTPCookieProcessor(cj)
    handlers.append(cjhdr)
    opener = urllib2.build_opener(*handlers)

    # Go to the login page. This sets initial cookies.
    loginURL = 'https://snow.traceup.com/login'
    html = requestHtml(opener, loginURL)

    # Post the login credentials.
    processLoginURL = 'https://snow.traceup.com/login'
    values = {'email': sys.argv[1], 'password': sys.argv[2], 'step': 'process'}
    data = urllib.urlencode(values)
    html = requestHtml(opener, processLoginURL, data)
    soup = BeautifulSoup(html, "html.parser")

    # Go to the GPX data export page.
    dataDownloadURL = 'http://snow.traceup.com/settings/gpx'
    html = requestHtml(opener, dataDownloadURL)
    soup = BeautifulSoup(html, "html.parser")

    for option in soup.find_all('option'):
        gpxURL = 'http://snow.traceup.com/settings/gpx'
        data = urllib.urlencode({'selected_visit': option.get('value')})
        request = urllib2.Request(gpxURL, data)
        gpxFile = opener.open(request)
        meta = gpxFile.info()
        disposition = meta.getheaders('Content-Disposition')
        fileName = disposition[0].split('; ')[1].replace('filename=', '')
        print('Downloading ' + fileName)
        with open('./' + fileName, 'wb') as output:
            output.write(gpxFile.read())


def main():
    scrapeIt()


if __name__ == '__main__':
    sys.exit(main())
