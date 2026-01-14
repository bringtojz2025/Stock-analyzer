#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix dashboard.py by removing the invalid last line"""

with open('dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove streamlit run line if it exists
if 'streamlit run dashboard.py' in content:
    content = content.replace('streamlit run dashboard.py\n', '')
    content = content.replace('streamlit run dashboard.py', '')

with open('dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Fixed: Removed streamlit run line from dashboard.py')
