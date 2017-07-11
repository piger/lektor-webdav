# -*- coding: utf-8 -*-
import os
import easywebdav
from lektor.pluginsystem import Plugin
from lektor.publisher import Publisher, PublishError


class WebdavPublisher(Publisher):
    def __init__(self, env, output_path):
        super(WebdavPublisher, self).__init__(env, output_path)
        self.username = env.webdav_username
        self.password = env.webdav_password
        self.remote_path = env.webdav_path

    def publish(self, target_url, credentials=None, **extra):
        cli = easywebdav.Client(target_url.host, protocol='https', username=self.username,
                                password=self.password, path=self.remote_path)

        # stolen from lektor-s3
        all_files = []
        for path, _, files in os.walk(self.output_path):
            for f in files:
                fullpath = os.path.join(path, f)
                relpath = os.path.relpath(fullpath, self.output_path)
                if not os.path.dirname(relpath).startswith(".lektor"):
                    all_files.append(os.path.relpath(fullpath, self.output_path))

        dirs = set([os.path.dirname(x) for x in all_files])
        dirs = [x for x in dirs if len(x)]
        dirs = sorted(dirs, key=lambda d: len(d))

        try:
            for d in dirs:
                if not cli.exists(d):
                    yield u"Creating directory '%s'" % d
                    cli.mkdirs(d)

            for f in all_files:
                local_f = os.path.join(self.output_path, f)
                yield u"Uploading file '%s'" % f
                cli.upload(local_f, f)

        except easywebdav.WebdavException as ex:
            self.fail(str(ex))

        yield u"Upload completed!"

    def fail(self, message):
        raise PublishError(message)


class WebdavPlugin(Plugin):
    name = u'webdav'
    description = u'Webdav upload support'

    def on_setup_env(self, **extra):
        config = self.get_config()
        self.env.webdav_username = config.get('username')
        self.env.webdav_password = config.get('password')
        self.env.webdav_path = config.get('path')

        self.env.add_publisher('webdav', WebdavPublisher)
