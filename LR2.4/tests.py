import unittest

import json_tests
import yaml_tests
import toml_tests

jsonTestSuite =  unittest.TestSuite()
jsonTestSuite.addTest(unittest.makeSuite(json_tests.TestSerializer))

yamlTestSuite =  unittest.TestSuite()
yamlTestSuite.addTest(unittest.makeSuite(yaml_tests.TestSerializer))

tomlTestSuite =  unittest.TestSuite()
tomlTestSuite.addTest(unittest.makeSuite(toml_tests.TestSerializer))

runner = unittest.TextTestRunner(verbosity = 2)
runner.run(jsonTestSuite)
print('\n')
runner.run(yamlTestSuite)
print('\n')
runner.run(tomlTestSuite)

