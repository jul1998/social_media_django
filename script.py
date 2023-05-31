import os
import sys
from django.core.management import call_command

# Set the Django environment
sys.path.append('backend\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend\backend.settings')

import django
django.setup()



# Run makemigrations and migrate
call_command('makemigrations')
call_command('migrate')