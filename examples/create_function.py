import lambdev


def main():
    response = lambdev.create(function_name='my_function_name',
                              runtime='python3.7',
                              role='arn:aws:iam::123456789012:role/example_role',
                              handler='my_script.lambda_handler',
                              description='my new lambda function'
                              )
    return response


if __name__ == '__main__':
    main()
