from rest_framework.parsers import JSONParser

from . import validation, http_responses
from .models import Content
from rest_framework.decorators import api_view

from .serializers import ImportContentSerializer, ExportContentSerializer


def folder_dfs(rez):
    folder_size = 0

    for i in range(len(rez['children'])):
        key = rez['children'][i]
        child = dict(ExportContentSerializer(Content.objects.get(pk=key)).data)
        rez['children'][i] = child
        if child['type'] == 'FOLDER':
            folder_dfs(child)
        elif child['type'] == 'FILE':
            child['children'] = None
        folder_size += child['size']

    rez['size'] = folder_size


@api_view(['GET'])
def get_content(request, uuid):
    content = validation.validation_get_request(uuid)
    if not content:
        return http_responses.get_404()
    content = ExportContentSerializer(content)
    rez = dict(content.data)
    if rez['type'] == 'FILE':
        rez['children'] = None
    elif rez['type'] == 'FOLDER':
        folder_dfs(rez)
    return http_responses.get_200(rez)


@api_view(['POST'])
def import_content(request):
    def add_item(item_id):
        item = get_item_by_id[item_id]
        try:
            item['date'] = import_data['updateDate']
            content = Content.objects.get(pk=item_id)
            if content.parentId_id is not None:
                parent = Content.objects.get(pk=content.parentId_id)
                if parent.type != 'FOLDER':
                    return False

            tmp_content = content
            while tmp_content.parentId_id is not None:
                tmp_content.date = item['date']
                tmp_content.save()
                tmp_content = Content.objects.get(pk=tmp_content.parentId_id)
            tmp_content.date = item['date']
            tmp_content.save()

            content = ImportContentSerializer(instance=content, data=item)
            if content.is_valid():
                content.save()
                return True
            return False

        except Content.DoesNotExist:
            item['date'] = import_data['updateDate']
            content_serializer = ImportContentSerializer(data=item)
            if content_serializer.is_valid():
                content_serializer.save()
                return True
            else:
                return False

    def dfs(v):
        if graph[v] in graph:
            is_checked[v] = True
            if get_item_by_id[graph[v]]['type'] == 'FOLDER':
                if is_checked[graph[v]] or dfs(graph[v]):
                    return add_item(v)
            return False
        else:
            if graph[v] is None:
                is_checked[v] = True
                return add_item(v)
            else:
                try:
                    content = Content.objects.get(pk=graph[v])
                    content = ImportContentSerializer(content)
                    if content.data['type'] == 'FOLDER':
                        is_checked[v] = True
                        return add_item(v)
                    return False
                except Content.DoesNotExist:
                    return False

    import_data = JSONParser().parse(request)
    if not validation.validation_import_data(import_data):
        return http_responses.get_400()
    items = import_data['items']
    # check parent-child hierarchy
    graph = {}
    is_checked = {}
    get_item_by_id = {}
    for item in items:
        if not validation.validation_elem(item):
            return http_responses.get_400()
        graph[item['id']] = item['parentId']
        is_checked[item['id']] = False
        get_item_by_id[item['id']] = item

    for v in graph:
        if not is_checked[v]:
            if not dfs(v):
                return http_responses.get_400()

    return http_responses.get_200({})


@api_view(['DELETE'])
def delete_content(request, uuid):
    try:
        content = Content.objects.get(pk=uuid)
        content.delete()
        return http_responses.get_200({})
    except Content.DoesNotExist:
        return http_responses.get_404()
