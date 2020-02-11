from setuptools import setup
setup(
    name='QQmail_recive',
    version='0.1',
    description='A realtime pop mail recever',
    url='http://github.com/Karobben/Python_Pop3_emial',
    author='Karobben',
    author_email='a591465908@outlook.com',
    license='MIT',
    install_requires=[
        'urwid',
        'poplib',
        'base64',
        'signal',
        'email',
        ],
    zip_safe=False,
    py_modules=['P_mail'],
    #????entry_points={ 'console_scripts': ['rtscli=rtscli:cli'] },
)
