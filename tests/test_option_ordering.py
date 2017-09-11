# coding: utf-8
# Copyright (c) 2016, 2017, Oracle and/or its affiliates. All rights reserved.

import unittest
from . import util


class TestOptionOrdering(unittest.TestCase):

    def setUp(self):
        util.set_admin_pass_phrase()

    def test_no_options(self):
        result = self.invoke_operation(['os', 'ns', 'get'])
        self.assertEqual(0, result.exit_code)
        assert not self.has_debug_data(result)

    def test_fail_unknown_options(self):
        result = self.invoke_operation(['iam', 'user', 'list', '--compartment-id', util.TENANT_ID, '--limit', '1', '--not-an-option'])
        self.assertNotEqual(0, result.exit_code)

        result = self.invoke_operation(['--not-an-option'])
        self.assertNotEqual(0, result.exit_code)

        result = self.invoke_operation(['iam', 'user', '-q'])
        self.assertNotEqual(0, result.exit_code)

    def test_debug_at_root(self):
        result = self.invoke_operation(['-d', 'os', 'ns', 'get'])
        self.assertEqual(0, result.exit_code)
        assert self.has_debug_data(result)

    def test_debug_at_service(self):
        result = self.invoke_operation(['os', '-d', 'ns', 'get'])
        self.assertEqual(0, result.exit_code)
        assert self.has_debug_data(result)

    def test_debug_at_noun(self):
        result = self.invoke_operation(['os', 'ns', '-d', 'get'])
        self.assertEqual(0, result.exit_code)
        assert self.has_debug_data(result)

    def test_debug_at_verb(self):
        result = self.invoke_operation(['os', 'ns', 'get', '-d'])
        self.assertEqual(0, result.exit_code)
        assert self.has_debug_data(result)

    def test_debug_with_command_option(self):
        result = self.invoke_operation(['iam', 'user', 'list', '--compartment-id', util.TENANT_ID, '--limit', '1', '-d'])
        self.assertEqual(0, result.exit_code)
        assert self.has_debug_data(result)

    def test_help_at_root(self):
        self.verify_help([], [None, '-?', '--help'], 'Usage: oci [OPTIONS]')

    def test_help_at_service(self):
        self.verify_help(['os'], [None, '-?', '--help'], 'Usage: oci os [OPTIONS]')

    def test_help_at_noun(self):
        self.verify_help(['os', 'ns'], [None, '-?', '--help'], 'Usage: oci os ns [OPTIONS]')

    def test_help_at_verb(self):
        self.verify_help(['os', 'ns', 'get'], ['-?', '--help'], 'Usage: oci os ns get [OPTIONS]')

    def invoke_operation(self, command):
        return util.invoke_command_as_admin(command)

    def has_debug_data(self, result):
        return 'send:' in result.output and 'Oracle-PythonSDK' in result.output

    def verify_help(self, command, help_commands, expected_output):
        """Runs the command with each of the possible help commands given, and verifies that in each case the output
        contains the expected string."""
        for help_command in help_commands:
            full_command = command
            if help_command:
                full_command = command + [help_command]

            result = self.invoke_operation(full_command)
            self.assertEqual(0, result.exit_code)
            assert expected_output in result.output


if __name__ == '__main__':
    unittest.main()
