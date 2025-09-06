#!/usr/bin/env python
"""
Simple script to compile Django message files without gettext tools
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pollution_tracker.settings')
django.setup()

# Try to compile messages
try:
    from django.core.management.commands.compilemessages import Command
    command = Command()
    command.handle()
    print("Messages compiled successfully!")
except Exception as e:
    print(f"Error compiling messages: {e}")
    print("You may need to install gettext tools or compile manually.")
