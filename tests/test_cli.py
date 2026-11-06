import json
import subprocess
import unittest
from unittest.mock import patch
import blank_canvas as app


class Tests(unittest.TestCase):
    def test_missing_access_is_unknown(self):
        self.assertEqual(app.summarize({})['agreement'], 'UNKNOWN')

    def test_authorization_does_not_hide_missing_agreement(self):
        result = app.summarize({'authorizationStatus': 'AUTHORIZED',
                                'agreementAvailability': {'status': 'NOT_AVAILABLE'}})
        self.assertEqual(result['agreement'], 'NOT_AVAILABLE')

    @patch('blank_canvas.shutil.which', return_value='/usr/bin/aws')
    def test_model_argument_is_never_shell_interpreted(self, _):
        model = 'model; echo unsafe'
        args = app.command('test', 'us-east-2', 'get-foundation-model-availability', model)
        self.assertEqual(args[-1], model)
        self.assertIn('test', args)
        self.assertIn('us-east-2', args)

    @patch('blank_canvas.subprocess.run', return_value=subprocess.CompletedProcess([], 254, '', 'AccessDenied'))
    @patch('blank_canvas.shutil.which', return_value='/usr/bin/aws')
    def test_aws_error_is_nonzero(self, _, run):
        self.assertEqual(app.main(['check', 'example']), 1)
        self.assertNotIn('shell', run.call_args.kwargs)

    @patch('blank_canvas.subprocess.run', return_value=subprocess.CompletedProcess([], 0, 'not-json', ''))
    @patch('blank_canvas.shutil.which', return_value='/usr/bin/aws')
    def test_malformed_response_is_nonzero(self, _, run):
        self.assertEqual(app.main(['models']), 1)

    @patch('blank_canvas.subprocess.run', side_effect=subprocess.TimeoutExpired('aws', 90))
    @patch('blank_canvas.shutil.which', return_value='/usr/bin/aws')
    def test_timeout_is_nonzero(self, _, run):
        self.assertEqual(app.main(['models']), 1)


if __name__ == '__main__':
    unittest.main()
