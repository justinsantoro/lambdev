import base64
import json
import unittest

from . import core

l = core.l


class LambdaError(Exception):
    pass


class LambdaTestFunction(unittest.TestCase):
    EXPECTED_RESPONSE = None
    TEST_OBJECT = None

    def test_function(self):
        self.assertEqual(run(payload=LambdaTestFunction.TEST_OBJECT, print_log=False), LambdaTestFunction.EXPECTED_RESPONSE)


def test(expected_response, test_object=None):
    print("- Testing...")
    LambdaTestFunction.EXPECTED_RESPONSE = expected_response
    LambdaTestFunction.TEST_OBJECT = test_object
    unittest.main()


# Publish function from $Latest. If desired alias already exists, update its version. If not, create it.
# Assumes by default that the latest version of code is already in $latest via lambdev.test()
def publish(alias, description='', upload=False):
    if upload:
        core.upload_package()

    fn = core.get_function_name()

    pubresponse = l.publish_version(FunctionName=fn)

    if core.alias_exists(l.list_aliases(FunctionName=fn), alias):
        print('- Alias already exists. Updating version...')
        aliasresponse = l.update_alias(FunctionName=core.get_function_name(),
                                       Name=alias,
                                       FunctionVersion=pubresponse['Version'])
        print('- Alias {} updated to version {}'.format(aliasresponse['Name'],
                                                  aliasresponse['FunctionVersion']))
    else:
        print('- Creating new alias: {}...'.format(alias))
        l.create_alias(FunctionName=fn,
                       Name=alias,
                       FunctionVersion=pubresponse['Version'],
                       Description=description)


def run(function_name=None, payload=None, print_log=True):
    if not function_name:
        function_name = core.get_function_name()
        core.upload_package()

    print("- Running {}...".format(function_name))
    response = l.invoke(FunctionName=function_name,
                        Payload=json.dumps(payload) if payload else None,
                        InvocationType='RequestResponse',
                        LogType='Tail' if print_log else 'None'
                        )

    if print_log:
        print(u'- Function log:\n{}'.format(base64.b64decode(response['LogResult']).decode('utf-8')))

    if 'FunctionError' in response:
        message = response['Payload'].read().decode('utf-8')
        if response['FunctionError'] == 'Handled':
            raise RuntimeError(message)
        else:
            raise LambdaError(message)
    else:
        return json.loads(response['Payload'].read().decode('utf-8'))


def create_function(function_name=None, role=None, handler=None, description=None, runtime='python3.7'):
    x = core.ProjectFolder(core.workingDir)
    print('- Creating function...')
    response = l.create_function(FunctionName=function_name,
                                 Runtime=runtime,
                                 Role=role,
                                 Handler=handler,
                                 Code={'ZipFile': x.build_zip()},
                                 Description=description,
                                 Publish=False
                                 )

    with open(core.workingDir + '/function_name.txt', 'w') as f:
        f.write(response['FunctionArn'])

    print('- Function Created')
