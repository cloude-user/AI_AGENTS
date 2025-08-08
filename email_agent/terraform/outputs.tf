output "ecr_repo_url" {
  value = aws_ecr_repository.gmail_agent_repo.repository_url
}

output "lambda_function_name" {
  value = aws_lambda_function.gmail_agent.function_name
}

output "event_rule_arn" {
  value = aws_cloudwatch_event_rule.gmail_agent_schedule.arn
}
