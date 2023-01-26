from .models import Content


def validation_get_request(uuid):
    try:
        return Content.objects.get(pk=uuid)
    finally:
        return False


def validation_import_data(import_data):
    if len(import_data) != 2 or 'items' not in import_data or 'updateDate' not in import_data:
        return False
    return True


def validation_elem(elem):
    for key in ('id', 'type'):
        if key not in elem:
            return False

    if elem['type'] == 'FOLDER':
        if 'size' in elem:
            if type(elem['size']) != int or elem['size'] != 0:
                return False
        else:
            elem['size'] = 0

    elif elem['type'] == 'FILE':
        if 'size' not in elem or type(elem['size']) != int or elem['size'] <= 0:
            return False
    else:
        return False

    if 'parentId' not in elem:
        elem['parentId'] = None

    return True
