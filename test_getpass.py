import getpass

try:
    pwd = getpass.getpass()
except Exception as ex:
    print('Error occurred : ', ex)
else:
    print('Entered secret :', pwd)