import os


def get_upload_path(instance, filename: str) -> str:
    name, extension = filename.split('.')
    return os.path.join(f'user/{instance.user.id}/{name}/')
