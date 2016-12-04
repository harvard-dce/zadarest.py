# -*- coding: utf-8 -*-

import pkg_resources  # part of setuptools
__version__ = pkg_resources.require("zadarest")[0].version

from zadarest import ZRestClient
from zadarest import ZError
from zadarest import ZConsoleClient
from zadarest import ZVpsaClient



