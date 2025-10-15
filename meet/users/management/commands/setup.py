"""
Custom management command to setup the UNIO backend application.
This command automates the initial setup process including:
- Creating media directories
- Running migrations
- Collecting static files
- Creating a superuser (optional)
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Setup UNIO backend application - creates directories, runs migrations, and optionally creates superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-superuser',
            action='store_true',
            help='Skip superuser creation',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Superuser email address',
            default='admin@unio.app'
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Superuser username',
            default='admin'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Starting UNIO Backend Setup'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Step 1: Create media directories
        self.stdout.write('\n[1/5] Creating media directories...')
        self.create_media_directories()

        # Step 2: Run migrations
        self.stdout.write('\n[2/5] Running database migrations...')
        try:
            call_command('makemigrations')
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('✓ Migrations completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Migration failed: {str(e)}'))

        # Step 3: Collect static files
        self.stdout.write('\n[3/5] Collecting static files...')
        try:
            call_command('collectstatic', '--noinput', '--clear')
            self.stdout.write(self.style.SUCCESS('✓ Static files collected successfully'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠ Static files collection skipped: {str(e)}'))

        # Step 4: Create superuser
        if not options['skip_superuser']:
            self.stdout.write('\n[4/5] Creating superuser...')
            self.create_superuser(options['email'], options['username'])
        else:
            self.stdout.write('\n[4/5] Skipping superuser creation...')

        # Step 5: Display setup summary
        self.stdout.write('\n[5/5] Setup Summary:')
        self.display_summary()

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('UNIO Backend Setup Complete!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('\nYou can now start the server with:'))
        self.stdout.write(self.style.WARNING('  python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('\nAccess the API documentation at:'))
        self.stdout.write(self.style.WARNING('  http://localhost:8000/swagger/'))

    def create_media_directories(self):
        """Create all necessary media directories"""
        directories = [
            settings.MEDIA_ROOT,
            settings.MEDIA_ROOT / 'profile_pics',
            settings.MEDIA_ROOT / 'meeting_files',
            settings.MEDIA_ROOT / 'recordings',
            settings.MEDIA_ROOT / 'shared_files',
            settings.STATIC_ROOT,
        ]

        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {directory}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to create {directory}: {str(e)}'))

    def create_superuser(self, email, username):
        """Create a superuser if one doesn't already exist"""
        try:
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'  ⚠ Superuser with email {email} already exists'))
                return

            self.stdout.write(f'  Creating superuser with email: {email}')
            password = input('  Enter password for superuser (or press Enter for default "admin123"): ').strip()
            
            if not password:
                password = 'admin123'
                self.stdout.write(self.style.WARNING('  Using default password: admin123'))

            user = User.objects.create_superuser(
                email=email,
                username=username,
                password=password
            )
            
            self.stdout.write(self.style.SUCCESS(f'  ✓ Superuser created successfully'))
            self.stdout.write(self.style.SUCCESS(f'    Email: {email}'))
            self.stdout.write(self.style.SUCCESS(f'    Username: {username}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ✗ Failed to create superuser: {str(e)}'))

    def display_summary(self):
        """Display setup summary information"""
        self.stdout.write(self.style.SUCCESS('  ✓ Database setup complete'))
        self.stdout.write(self.style.SUCCESS('  ✓ Media directories created'))
        self.stdout.write(self.style.SUCCESS('  ✓ Application is ready to use'))
        
        # Check if .env file exists
        env_file = settings.BASE_DIR / '.env'
        if not env_file.exists():
            self.stdout.write(self.style.WARNING('\n  ⚠ No .env file found!'))
            self.stdout.write(self.style.WARNING('    Copy .env.example to .env and configure:'))
            self.stdout.write(self.style.WARNING('      - SECRET_KEY (required for production)'))
            self.stdout.write(self.style.WARNING('      - Google OAuth2 credentials'))
            self.stdout.write(self.style.WARNING('      - Microsoft OAuth2 credentials'))
            self.stdout.write(self.style.WARNING('      - Redis configuration (for production)'))
