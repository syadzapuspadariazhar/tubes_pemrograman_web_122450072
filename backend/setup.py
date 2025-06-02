from setuptools import setup

setup(
    name='budget_api',
    install_requires=[
        'pyramid',
        'sqlalchemy',
        'pyramid_tm',
        'waitress',
        'psycopg2-binary',
    ],
    entry_points={
        'paste.app_factory': [
            'main = app.__init__:main',
        ],
    },
)
