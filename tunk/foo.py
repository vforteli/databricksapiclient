from argparser import parse_params, concat_path


params = {"some_param": "blabla"}

result = parse_params(params)

print(result)


path = concat_path("fooo/", "/tunk/", "/foo.py")


print(path)
