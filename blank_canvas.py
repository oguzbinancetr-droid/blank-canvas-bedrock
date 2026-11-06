"""Blank Canvas: read-only Amazon Bedrock model access diagnostics."""
import argparse
import json
import shutil
import subprocess
import sys


def summarize(data):
    return {
        'model': data.get('modelId'),
        'agreement': data.get('agreementAvailability', {}).get('status', 'UNKNOWN'),
        'authorization': data.get('authorizationStatus', 'UNKNOWN'),
        'entitlement': data.get('entitlementAvailability', 'UNKNOWN'),
        'region': data.get('regionAvailability', 'UNKNOWN'),
        'note': 'Catalog visibility and IAM authorization do not prove invocation access.',
    }


def command(profile, region, operation, model=None):
    executable = shutil.which('aws')
    if not executable:
        raise RuntimeError('Install AWS CLI v2 and authenticate with aws login first.')
    args = [executable, 'bedrock', operation, '--profile', profile,
            '--region', region, '--output', 'json', '--no-cli-pager']
    if model:
        args.extend(['--model-id', model])
    return args


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', default='blank-canvas')
    parser.add_argument('--region', default='us-east-2')
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('models', help='List the regional catalog without inference')
    check = sub.add_parser('check', help='Read model access metadata without inference')
    check.add_argument('model')
    args = parser.parse_args(argv)
    try:
        operation = 'list-foundation-models' if args.action == 'models' else 'get-foundation-model-availability'
        result = subprocess.run(command(args.profile, args.region, operation, getattr(args, 'model', None)),
                                capture_output=True, text=True, timeout=90)
        if result.returncode:
            print(result.stderr.strip() or 'AWS command failed', file=sys.stderr)
            return 1
        data = json.loads(result.stdout)
        if args.action == 'check':
            data = summarize(data)
        else:
            data = [{'id': m['modelId'], 'name': m['modelName'],
                     'inferenceTypes': m.get('inferenceTypesSupported', []),
                     'lifecycle': m.get('modelLifecycle', {}).get('status', 'UNKNOWN')}
                    for m in data.get('modelSummaries', [])]
        print(json.dumps(data, indent=2))
        return 0
    except (RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
