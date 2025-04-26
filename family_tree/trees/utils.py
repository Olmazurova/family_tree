
def form_valid_base(form):
    new_person = form.instance
    new_person.save()

    if new_person.spouse:
        spouse = new_person.spouse
        spouse.spouse = new_person
        spouse.save()

    return new_person
