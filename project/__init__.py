import os
import django

def run_migrations():
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
        django.setup()
        from django.core.management import call_command
        call_command('migrate', interactive=False)
    except Exception as e:
        print("マイグレーション失敗:", e)

run_migrations()
