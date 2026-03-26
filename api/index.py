# -*- coding: utf-8 -*-
"""Vercel entry point for Xiaoxiao News Flask App"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wechat_work_backend import app

# Vercel requires this
handler = app
