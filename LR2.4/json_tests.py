import unittest

import serializer
import test_objects


class TestSerializer(unittest.TestCase):

    def test_json_string(self):

        json_str = serializer.dumps(test_objects.string, 'json')
        des_str = serializer.loads(json_str, 'json')

        self.assertEqual(test_objects.string, des_str)


    def test_json_list(self):

        json_list = serializer.dumps(test_objects.list, 'json')
        des_list = serializer.loads(json_list, 'json')

        self.assertEqual(test_objects.list, des_list)

    
    def test_json_dict(self):

        json_dict = serializer.dumps(test_objects.dict, 'json')
        des_dict = serializer.loads(json_dict, 'json')

        self.assertEqual(test_objects.dict, des_dict)


    def test_json_class(self):

        json_class = serializer.dumps(test_objects.MyClass, 'json')
        deserialized_class = serializer.loads(json_class, 'json')

        self.assertEqual(deserialized_class.a, test_objects.MyClass.a)
        self.assertEqual(deserialized_class.my_func(1), test_objects.MyClass.my_func(1))


    def test_json_func(self):

        json_func = serializer.dumps(test_objects.func, 'json')
        des_func = serializer.loads(json_func, 'json')

        self.assertEqual(test_objects.func(2), des_func(2))
        

    def test_json_lambda(self):

        json_lmbd = serializer.dumps(test_objects.lmbd, 'json')
        des_lmbd = serializer.loads(json_lmbd, 'json')

        self.assertEqual(test_objects.lmbd(1), des_lmbd(1))


    def test_json_func_with_defaults(self):

        json_func = serializer.dumps(test_objects.func_with_defaults, 'json')
        des_func = serializer.loads(json_func, 'json')

        self.assertEqual(test_objects.func_with_defaults(), des_func())
