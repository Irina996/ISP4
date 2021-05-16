# import serializer
# import yaml_serializer
# import json_deserializer

# a = 3
# def func(x):
#     return x + a


# class Test:
#     var = 3
#     def Sum(x, y):
#         return x+y


# lmbd = lambda c: c + 10

# y = serializer.dumps(lmbd, 'yaml')
# print(y)
# j = yaml_serializer._yaml_to_json(y)
# print(j)

# j = serializer.dumps(lmbd, 'json')
# print("\n", j)
# l_y = serializer.loads(y, 'yaml')

# # yaml_func = serializer.dumps(func, 'yaml')
# # des_func = serializer.loads(yaml_func, 'yaml')
# # a = a + 5
# # print(yaml_func)
# # if func(2) == des_func(2) + 5:
# #     print('OK')

# # j = serializer.dumps(Test, 'json')
# # cl_j = serializer.loads(j, 'json')
# # print(cl_j.Sum(1, 2))

# # y = serializer.dumps(Test, 'yaml')
# # cl_y = serializer.loads(y, 'yaml')
# # print(cl_y.Sum(1, 2))

# # t = serializer.dumps(Test, 'toml')
# # cl_t = serializer.loads(t, 'toml')
# # print(cl_t.Sum(1, 2))


# #test2

# # j = serializer.dumps(Test, 'json')
# # print(j)
# # f_j = serializer.loads(j, 'json')

# # y = serializer.dumps(Test, 'yaml')
# # print('\n', y)
# # f_y = serializer.loads(y, 'yaml')

# # t = serializer.dumps(Test, 'toml')
# # print('\n', t)
# # f_t = serializer.loads(t, 'toml')

# # print(f_j.Sum(1, 2))
# # print(f_y.Sum(2, 3))
# # print(f_t.Sum(3, 4))



# # test1

# # j = serializer.dumps(func, 'json')
# # f_j = serializer.loads(j, 'json')

# # y = serializer.dumps(func, 'yaml')
# # f_y = serializer.loads(y, 'yaml')

# # t = serializer.dumps(func, 'toml')
# # f_t = serializer.loads(t, 'toml')

# # a = 10

# # print(f_j(3))
# # print(f_y(3))
# # print(f_t(3))