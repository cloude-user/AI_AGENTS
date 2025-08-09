# Lambda Function (container image)
resource "aws_lambda_function" "gmail_agent" {
  function_name = "gmail-agent"
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = "${var.ecr_uri}:${var.image_tag}"

  memory_size = 1536
  timeout     = 300

  environment {
    variables = {
      OPENAI_API_KEY = var.OPENAI_API_KEY,
      GMAIL_TOKEN = var.GMAIL_TOKEN,
      GMAIL_REFRESH_TOKEN = var.GMAIL_REFRESH_TOKEN,
      GMAIL_CLIENT_ID = var.GMAIL_CLIENT_ID,
      GMAIL_CLIENT_SECRET = var.GMAIL_CLIENT_SECRET

    }
  }

  depends_on = [aws_iam_role_policy_attachment.lambda_basic_exec]
}

# EventBridge rule: daily at 10:00 AM UTC
resource "aws_cloudwatch_event_rule" "gmail_agent_schedule" {
  name                = "gmail-agent-daily-10am-utc"
  description         = "Run Gmail Agent once a day at 10:00 AM UTC"
  schedule_expression = "cron(0 */15 * * ? *)"
}

resource "aws_cloudwatch_event_target" "gmail_agent_target" {
  rule      = aws_cloudwatch_event_rule.gmail_agent_schedule.name
  target_id = "GmailAgentLambda"
  arn       = aws_lambda_function.gmail_agent.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.gmail_agent.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.gmail_agent_schedule.arn
}