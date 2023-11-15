from pizzad.models.pattern import Registry, Memento


def save_registry_to_memento(caretaker, registry: Registry, strategy):
    pass


def save_memento_to_file(caretaker, memento: Memento, strategy, file):
    pass


def restore_memento_from_file(caretaker, file, strategy):
    pass


def restore_registry_from_memento(caretaker, memento, strategy):
    pass
