#!/usr/bin/env python3
import os
import urllib.request

fp = urllib.request.urlopen("http://localhost:5000/customer/customer-1")

encodedContent = fp.read()
decodedContent = encodedContent.decode("utf8")

print(decodedContent)

fp.close()
