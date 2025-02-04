# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# CSV-file downloader
# First line is a field names
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import csv
import gzip

# Third-party modules
import six

# NOC modules
from noc.main.refbooks.downloaders import Downloader as DownloaderBase
from noc.core.http.client import fetch_sync


class Downloader(DownloaderBase):
    """
    Download reference book from CSV file
    First line of CSV file is field names
    """

    name = "CSV"

    @classmethod
    def download(cls, ref_book):
        out = []
        # Fetch data into StringIO wrapper
        url = ref_book.download_url
        url = url.replace("http://update.nocproject.org/db/", "https://cdn.nocproject.org/refbook/")
        code, headers, body = fetch_sync(url, follow_redirects=True, allow_proxy=True)
        if code != 200:
            raise IOError("Invalid HTTP response: %s" % code)

        data = six.StringIO(body)
        # Wrap GzipFile for gzipped content
        if ref_book.download_url.endswith(".gz"):
            data = gzip.GzipFile(fileobj=data)
        # Iterate through CSV
        reader = csv.reader(data)
        header = {}
        for row in reader:
            if not row:
                continue
            if not header:
                # Read field names from first line
                for i, h in enumerate(row):
                    header[i] = unicode(h, "utf8", "ignore")
                continue
            r = {}
            for i, v in enumerate(row):
                r[header[i]] = unicode(v, "utf8", "ignore")
            out.append(r)
        return out
