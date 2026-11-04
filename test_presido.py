from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, DeanonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# 1. Initialize all three core engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
deanonymizer = DeanonymizerEngine()

# Secrets for encryption (Must be exactly 16, 24, or 32 characters long)
SECRET_CRYPTO_KEY = "1234567890123456" 

text_to_scrub = "Hello, my name is John Doe and my phone number is 212-555-0199."
print(f"--- 1. Original Transcript ---\n{text_to_scrub}\n")

# 2. Analyze the text for specific PII
analysis_results = analyzer.analyze(
    text=text_to_scrub, 
    language="en",
    entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS"]
)

# 3. ANONYMIZE: Encrypt the PII tokens so they are hidden but reversible
anonymized_result = anonymizer.anonymize(
    text=text_to_scrub, 
    analyzer_results=analysis_results,
    operators={"DEFAULT": OperatorConfig("encrypt", {"key": SECRET_CRYPTO_KEY})}
)

print(f"--- 2. Safe Text (Send this to the LLM) ---\n{anonymized_result.text}\n")

# -------------------------------------------------------------------------
# SIMULATION: Imagine sending the safe text to an LLM, and it replies back:
# "The user named [Encrypted...] wants a callback at [Encrypted...]."
# -------------------------------------------------------------------------
llm_response = f"Acknowledged. The user {anonymized_result.text}" 

# 4. DEANONYMIZE: Decrypt the text back to its original form using the saved items mapping
restored_result = deanonymizer.deanonymize(
    text=llm_response,
    anonymizer_results=anonymized_result.items,
    operators={"DEFAULT": OperatorConfig("decrypt", {"key": SECRET_CRYPTO_KEY})}
)

print(f"--- 3. Restored Final Output (For Internal Display) ---\n{restored_result.text}")
