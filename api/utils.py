import json
import os

from rest_framework import status
from rest_framework.response import Response

from api.models import Task, User, Channel
from TodoList.settings import BASE_DIR


def response(data, to_channel=False, code=status.HTTP_200_OK):
    """
    Overrides rest_framework response
    :param data: data to be send in response
    :param to_channel: to post the response into the channel
    :param code: response status code(default has been set to 200)
    """
    resp_type = "in_channel" if to_channel else "ephemeral"
    res = {
        "response_type": resp_type,
        "text": data
    }
    log('info', res)
    return Response(data=res, status=code)


def log(level, data):
    """
    To log data in log.txt file
    :param level: info, error, debug
    :param data: data
    :return: None
    """
    level_map = {
        'info': 'INFO',
        'debug': 'DEBUG',
        'error': 'ERROR',
    }
    try:
        file_path = os.path.join(BASE_DIR, 'log.txt')
        if not os.path.exists(file_path):
            open(file_path, 'a+').close()
        with open(file_path, 'a+') as logger:
            size = logger.tell() / (1024 * 1024)
            if size > 2:
                logs = logger.read().splitlines()
            if isinstance(data, dict):
                data = json.dumps(data)
            logger.write("# [ " + level_map.get(level.lower(), 'DEFAULT') + " ] | " + data + '\n\n')
        if size > 10:
            os.remove(file_path)
            del logs[:10]
            with open(file_path, 'w') as logger:
                for line in logs:
                    logger.write('%s\n' % line)
    except Exception as e:
        pass


def create_user_and_channel(params):
    """
    To create user and channel before all apis
    :param params:
                - user_id
                - user_name
                - team_id
                - team_name
                - channel_id
                - channel_name
    :return: user, channel
    """
    log('info', {"params": params, "msg": "In create_user_and_channel utils"})
    user_id = params.get('user_id', '')
    user_name = params.get('user_name', '')
    team_id = params.get('team_id', '')
    team_name = params.get('team_name', '')
    channel_id = params.get('channel_id', '')
    channel_name = params.get('channel_name', '')
    user, created = User.objects.get_or_create(user_id=user_id, user_name=user_name, team_id=team_id,
                                               team_name=team_name)
    channel, created = Channel.objects.get_or_create(channel_id=channel_id, channel_name=channel_name)
    channel.user.add(user)
    return user, channel


def add_task(params, request):
    """
    Add task in database
    :param params: request.data
    :param request: Django request
    :return: None
    """
    log('info', {"params": params, "msg": "In add task utils"})
    task = params.get('text', '')
    user, channel = create_user_and_channel(params)
    task, created = Task.objects.get_or_create(created_by=user, task_name=task, created_in=channel)
    if created:
        return response(data='Added TODO for \'%s\'.' % (task, ), to_channel=True)
    if not task.is_deleted:
        return response(data='Already added TODO for \'%s\'.' % (task, ), to_channel=True)
    task.is_deleted = False
    task.save()
    return response(data='Added TODO for \'%s\'.' % (task,), to_channel=True)


def show_tasks(params, request):
    """
    Show all tasks of the channel
    :param params: request.data
    :param request: Django request
    :return: None
    """
    log('info', {"params": params, "msg": "In show tasks utils"})
    user, channel = create_user_and_channel(params)
    tasks = Task.objects.filter(created_in=channel, is_deleted=False).values_list('task_name', flat=True)
    if not tasks.count():
        return response(data="No TODOs", to_channel=True)
    data = ""
    for i in tasks:
        data += "- " + i + "\n"
    data = data.strip('\n')
    return response(data, to_channel=True)


def remove_task(params, request):
    """
    Remove the specific task
    :param params: request.data
    :param request: Django request
    :return: None
    """
    log('info', {"params": params, "msg": "In remove task utils"})
    task = params.get('text', '')
    user, channel = create_user_and_channel(params)
    try:
        task = Task.objects.get(task_name=task, created_in=channel, is_deleted=False)
    except Task.DoesNotExist as e:
        return response(data="\'%s\' is not present in TODO." % (task, ), to_channel=True)
    if task.created_in in user.channel_users.all():
        task.delete()
        return response(data="Removed TODO for \'%s\'." % (task, ), to_channel=True)
    else:
        return response("\'%s\' does not have permission to delete the TODO" % (user.user_name, ), to_channel=True)
