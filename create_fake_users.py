# import os
# import sys
# import django
# from faker import Faker

# # Django setup
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialproject.settings')
# django.setup()

# from users.models import User  # Passe diesen Import an dein User-Modell an

# # Faker instance
# fake = Faker()

# # Create 30 fake users
# for _ in range(30):
#     user = User(
#         username=fake.user_name(),
#         first_name=fake.first_name(),
#         last_name=fake.last_name(),
#         email=fake.email(),
#         # Füge hier weitere Felder hinzu, die dein User-Modell benötigt
#     )
#     user.set_password(fake.password())
#     user.save()

# print("30 Fake-User wurden erfolgreich erstellt.")


#Profile erstellen

import os
import sys
import django
from faker import Faker

# Projektstammverzeichnis zum Python-Pfad hinzufügen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialproject.settings')
django.setup()

from users.models import User, Profile  # Passe diesen Import an dein User- und Profil-Modell an

# Faker instance
fake = Faker()

# Create profiles for users who don't have one
users_without_profile = User.objects.filter(profile__isnull=True)

for user in users_without_profile:
    profile = Profile(
        user=user,
        photo='users/images/user.png',  # Hier kannst du einen Standardpfad oder Fake-Bilddaten hinzufügen, wenn nötig
        bio=fake.text(max_nb_chars=100)
    )
    profile.save()

print(f"Profile für {users_without_profile.count()} Benutzer wurden erfolgreich erstellt.")