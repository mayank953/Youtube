# parallel_demo.py  – run with:  python parallel_demo.py "Translate: Hello, world!"
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

GEMINI = "gemini-2.0-flash"

def make_translator_agent(lang_code, output_key):
    return LlmAgent(
        name=f"Translator_{lang_code}",
        model=GEMINI,
        instruction=f"Translate the user prompt into {lang_code}. "
                    "Return ONLY the translation text.",
        output_key=output_key,
    )

# 1️⃣ Three independent translators
spanish = make_translator_agent("Spanish", "es")
french  = make_translator_agent("French",  "fr")
german  = make_translator_agent("German",  "de")

parallel_translate = SequentialAgent(
    name="ParallelTranslate",
    sub_agents=[spanish, french, german],
    description="Runs three translation agents in Sequence."
)


root_agent = parallel_translate

# # 2️⃣ Merge their outputs for readability
# merger = LlmAgent(
#     name="Merger",
#     model=GEMINI,
#     instruction=(
#         "Package the translations neatly:\n"
#         "**Spanish:** {es}\n**French:** {fr}\n**German:** {de}"
#         "\nReturn exactly that block."
#     )
# )

# pipeline = SequentialAgent(
#     name="TranslatePipeline",
#     sub_agents=[parallel_translate, merger],
# )

# root_agent = pipeline
