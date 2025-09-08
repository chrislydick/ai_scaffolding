package terraform.security

default deny = []

waived(rule, name) {
  some w
  w := input.waivers[_]
  w.rule == rule
  w.resource == name
  not expired(w.expires)
}

expired(date) {
  # expects YYYY-MM-DD; treat missing as expired false
  not date
  false
}

expired(date) {
  date
  now := time.now_ns()
  ts := time.parse_rfc3339_ns(sprintf("%sT23:59:59Z", [date]))
  now > ts
}

# Require SSE on S3 buckets
deny[msg] {
  rc := input.resource_changes[_]
  rc.type == "aws_s3_bucket"
  name := rc.name
  not rc.change.after.server_side_encryption_configuration
  not waived("require-sse", name)
  msg := sprintf("[require-sse] S3 bucket %q must enable SSE", [name])
}

# Forbid Action: * in IAM policies
deny[msg] {
  rc := input.resource_changes[_]
  startswith(rc.type, "aws_iam_")
  name := rc.name
  some i
  stmt := rc.change.after.policy_document.Statement[i]
  stmt.Action == "*"
  not waived("no-iam-star", name)
  msg := sprintf("[no-iam-star] IAM %q must not allow Action: *", [name])
}

