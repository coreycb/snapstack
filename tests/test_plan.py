import os
import mock
import unittest

from snapstack import Plan


class TestRunner(unittest.TestCase):

    @mock.patch('snapstack.plan.subprocess')
    @mock.patch('snapstack.step.subprocess')
    def test_faux_run(self, mock_subprocess, mock_subprocess_plan):
        '''
        _test_faux_run

        Test to verify that it looks like we are going to run all the
        right scripts, without actually setting up a snapstack.

        '''
        # Pick something in the base to test, so we don't actually
        # need to fake out tests for it:
        plan = Plan()

        faux_p = mock.Mock()
        faux_p.returncode = 0

        env = dict(os.environ)
        env.update({'BASE_DIR': plan.tempdir})

        mock_subprocess.run.return_value = faux_p
        mock_subprocess_plan.run.return_value = faux_p

        plan.run(cleanup=False)  # Tempdir will cleanup itself.

        self.assertTrue(
            os.path.exists(os.sep.join([plan.tempdir, 'admin-openrc'])))

        mock_subprocess.run.assert_called_with(
            [os.sep.join([plan.tempdir, 'scripts/neutron-ext-net.sh'])],
            env=env)

        plan.run()  # Run plan again with cleanup
        mock_subprocess.run.assert_called_with(['sql_cleanup.py'], env=env)

    @unittest.skipUnless(
        os.environ.get('SNAPSTACK_TEST_INSTALL'),
        'Enabling this test will install software and tools on your machine.')
    def test_real_run(self):
        '''
        _test_real_run

        Comment out the skip above to setup snapstack on this machine.

        '''
        plan = Plan()
        plan.run()
