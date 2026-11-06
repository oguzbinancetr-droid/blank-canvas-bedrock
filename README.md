# Blank Canvas — Bedrock Developer Starter

A personal software development project exploring Amazon Bedrock and Claude Code for coding, code review, testing, and debugging. Includes a small, auditable CLI for diagnosing model access before attempting paid inference.

## Implemented

- Regional model catalog with model IDs, lifecycle, and inference types
- Separate agreement, IAM authorization, entitlement, and regional availability diagnostics
- Explicit AWS profile and Region selection
- Process timeouts, nonzero error exits, and offline unit tests
- GitHub Actions CI across Python 3.10, 3.12, and 3.13

This CLI is read-only: it does not invoke models, create subscriptions, submit forms, or modify IAM. No successful Claude inference is claimed. Catalog visibility does not establish permission to invoke a model.

## Getting started

Requires Python 3.10+ and a current AWS CLI v2. No Python packages are needed.

```bash
aws login --profile blank-canvas --region us-east-2
python3 blank_canvas.py models
python3 blank_canvas.py check anthropic.claude-haiku-5-5
python3 blank_canvas.py --profile YOUR_PROFILE --region YOUR_ASSIGNED_REGION models
```

Use your own project's assigned Region. The new AWS experience restricts cross-Region features. This tool does not attempt cross-Region inference or bypass regional restrictions.

## Understanding results

| Field | Meaning |
| --- | --- |
| agreement | Model agreement status; NOT_AVAILABLE means no active access agreement |
| authorization | Whether the principal is authorized according to the availability API |
| entitlement | Model entitlement metadata |
| region | Whether the model is offered in the selected Region |

Even AVAILABLE metadata is not proof of a successful inference call. Anthropic models can require a first-use form, Marketplace prerequisites, and additional project-specific access. Follow the actual AWS error message; do not fix access failures by granting unrestricted IAM permissions.

## Claude Code

Install Claude Code using the official quickstart, run `claude`, and select **3rd-party platform → Amazon Bedrock**. Select your own AWS profile and assigned Region. Existing installations can run `/setup-bedrock`. Claude Code is a separate application; this CLI checks prerequisites, not its session state.

Model usage is billed separately. Verify credit eligibility and spending in AWS Settings → Billing. Credits do not automatically grant model access. This repository neither promises free inference nor changes billing plans.

## Development

```bash
python3 -m unittest discover -s tests -v
python3 blank_canvas.py --help
```

Tests run offline with mocked AWS processes. No AWS credentials or paid model calls are required. API errors and malformed responses return a nonzero exit code. All arguments are passed without a shell.

## Security

Use temporary AWS login credentials. Never commit API keys, AWS login caches, or credential files. The CLI does not persist tokens or model conversations. AWS error messages may contain project identifiers; redact them before sharing publicly. Report vulnerabilities privately to the repository owner without including secrets.

## References

- [AWS model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- [Claude Code quickstart](https://code.claude.com/docs/en/quickstart)
- [Claude Code on Bedrock](https://code.claude.com/docs/en/amazon-bedrock)
- [AWS project Regions](https://docs.aws.amazon.com/accounts/latest/reference/project-regions.html)

Independent personal project; not an AWS or Anthropic product.
