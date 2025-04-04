from django.contrib.auth import get_user_model
from django.db.models import Min

from .models import Person

User = get_user_model()


def change_owner_or_delete():
    pass


def setting_level(person, tree):
    generation = Person.objects.filter(genus_name=tree.id).aggregate(Min('level', default=0))
    if person.parents.all().count():
        person.level = (person.parents.first().level or 0) + 1
    elif person.spouse:
        person.level = person.spouse.level
    else:
        person.level = generation['level__min']
    person.save()



def get_progenitor():
    pass