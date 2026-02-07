from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.tools.tool_context import ToolContext

GEMINI_MODEL = "gemini-2.0-flash"


def exit_loop(tool_context: ToolContext):
    """Signal the loop to stop when the SQL query is correct and efficient."""
    tool_context.actions.escalate = True
    return {}


code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model=GEMINI_MODEL,
    instruction=(
        "You are an SQL Query Generator. "
        "Based only on the user's request, write a single SQL query that fulfills the requirement. "
        "Output only the complete SQL query as a code block, enclosed in triple backticks (```sql ... ```). "
        "Do not add any other text before or after the code block."
    ),
    description="Writes an initial SQL query based on a specification.",
    output_key="current_code"
)

code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model=GEMINI_MODEL,
    instruction=(
        "You are an expert SQL Reviewer. "
        "Review the following SQL and provide concise feedback. "
        "If it is correct, safe, and efficient, call the exit_loop tool.\n\n"
        "SQL to Review:\n"
        "```sql\n"
        "{current_code}\n"
        "```\n\n"
        "Review Criteria (bulleted, concise):\n"
        "1. Correctness (joins/filters/grouping)\n"
        "2. Safety (avoid injection patterns)\n"
        "3. Performance (selectivity, avoid unnecessary scans)\n"
        "4. Readability (aliases, casing, formatting)\n"
        "5. Edge Cases (NULLs, duplicates)\n\n"
        "Output only the review bullets or the sentence: \"No major issues found.\" "
        "If the query meets all conditions, call exit_loop."
    ),
    description="Reviews SQL and provides feedback or ends the loop when ready.",
    output_key="review_comments",
    tools=[exit_loop]
)

code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model=GEMINI_MODEL,
    instruction=(
        "You are an SQL Query Refactoring AI. "
        "Apply the review comments to improve the SQL below. "
        "If the comments say \"No major issues found.\", return the original SQL unchanged.\n\n"
        "Original SQL:\n"
        "```sql\n"
        "{current_code}\n"
        "```\n\n"
        "Review Comments:\n"
        "{review_comments}\n\n"
        "Output only the final SQL query as a code block, enclosed in triple backticks (```sql ... ```). "
        "Do not add any other text before or after the code block."
    ),
    description="Refactors SQL based on review comments.",
    output_key="current_code"
)

refinement_loop = LoopAgent(
    name="CodeRefinementLoop",
    description="Iteratively reviews and refactors SQL until quality checks pass.",
    sub_agents=[code_reviewer_agent, code_refactorer_agent],
    max_iterations=5
)

CodeGenerationPipeline = SequentialAgent(
    name="CodeSequentialPipeline",
    description="Generates an SQL query, then loops through review and refactor cycles until it passes.",
    sub_agents=[code_writer_agent, refinement_loop]
)

root_agent = CodeGenerationPipeline

