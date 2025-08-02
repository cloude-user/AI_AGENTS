resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "email-cleaner-daily"
  schedule_expression = "cron(0 18 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "emailCleaner"
  arn       = aws_lambda_function.email_cleaner.arn
}

