from setuptools import setup

setup(
    name='lektor-webdav',
    version='0.1',
    author=u'Daniel Kertesz',
    author_email='daniel@spatof.org',
    license='MIT',
    py_modules=['lektor_webdav'],
    install_requires=[
        'easywebdav',
    ],
    entry_points={
        'lektor.plugins': [
            'webdav = lektor_webdav:WebdavPlugin',
        ]
    }
)
