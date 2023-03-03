
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pet_kare.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()


# pet_data = {"name": "Beethoven", "age": 1, "weight": 30, "sex": "Male"}
# # Criação da instancia de Pet
# p1 = Pet(**pet_data)

# # Criação e persistindo o grupo
# group_data = {"scientific_name": "canis familiaris"}
# g1 = Group.objects.create(**group_data)

# # Associando o grupo ao pet e persistindo o pet
# p1.group = g1
# p1.save()


# # Criação e persistência das características
# trait_1_data = {"name": "curious"}
# trait_2_data = {"name": "hairy"}
# t1 = Trait.objects.create(**trait_1_data)
# t2 = Trait.objects.create(**trait_2_data)

# # Associando as características ao pet
# p1.traits.add(t1)
# p1.traits.add(t2)

# # Tentando deletar um grupo associado a pets
# g1.delete()
# # ProtectedError