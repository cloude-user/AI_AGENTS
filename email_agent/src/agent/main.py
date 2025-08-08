from agent.agent_graph import agent_executor

if __name__ == "__main__":
    print("🚀 Running Email Agentic Cleaner")
    final_state = agent_executor.invoke({})
    print("✅ Agent Finished. Final state:")
    print(final_state)

# from agent.tools.classifier import classify_email
# from agent.tools.delete_email import delete_email
# from agent.tools.draft_reply import generate_draft_reply
# from agent.tools.notifier import notify_user

# def main():
#     # 1. Simulate an incoming email (as if fetched from Gmail)
#     sample_email = {
#         "id": "123",
#         "snippet": "Exciting job opportunity for DevOps engineers at ABC Corp!",
#         "payload": {
#             "headers": [
#                 {"name": "Subject", "value": "Job Opening: DevOps Engineer"},
#                 {"name": "From", "value": "hr@abccorp.com"},
#                 {"name": "To", "value": "you@example.com"},
#             ]
#         }
#     }

#     print("\n[Step 1] Incoming Email Received")
#     print("Subject:", sample_email["payload"]["headers"][0]["value"])

#     # 2. Classify the email
#     classification = classify_email(sample_email)
#     print("\n[Step 2] Classified as:", classification)

#     if classification == "promotion":
#         # 3. Delete promotional emails
#         delete_email(sample_email)
#         print("[Step 3] Promotional email deleted.")
#     elif classification == "job_opportunity":
#         # 4. Draft a reply for job-related email
#         draft = generate_draft_reply(sample_email)
#         print("[Step 4] Drafted reply:\n", draft)

#         # 5. Notify user
#         notify_user(sample_email, draft)
#         print("[Step 5] User notified.")

# if __name__ == "__main__":
#     main()

