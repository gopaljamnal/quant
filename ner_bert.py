from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification
import torch
# # Initialize the NER pipeline
# ner_pipeline = pipeline("ner",
#                         model="dbmdz/bert-large-cased-finetuned-conll03-english",
#                         aggregation_strategy="simple")
#
# # Text example
# text = "Apple CEO Tim Cook announced new iPhone models in California yesterday."
#
# # Perform NER
# entities = ner_pipeline(text)
#
# # Print the results
# for entity in entities:
#     print(f"Entity: {entity['word']}")
#     print(f"Type: {entity['entity_group']}")
#     print(f"Confidence: {entity['score']:.4f}")
#     print("-" * 30)


# from transformers import AutoTokenizer, AutoModelForTokenClassification
# import torch

# Load model and tokenizer
model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Text example
text = "Google and Microsoft are competing in the AI space while Elon Musk founded SpaceX."

# Tokenize the text
inputs = tokenizer(text, return_tensors="pt", add_special_tokens=True)

# Get predictions
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)

# Convert predictions to labels
label_list = model.config.id2label
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
predictions = predictions[0].tolist()

# Process results
current_entity = []
current_entity_type = None

for token, prediction in zip(tokens, predictions):
    if token.startswith("##"):
        if current_entity:
            current_entity.append(token[2:])
    else:
        if current_entity:
            print(f"Entity: {''.join(current_entity)}")
            print(f"Type: {current_entity_type}")
            print("-" * 30)
            current_entity = []

        if label_list[prediction] != "O":
            current_entity = [token]
            current_entity_type = label_list[prediction]

# Print final entity if exists
if current_entity:
    print(f"Entity: {''.join(current_entity)}")
    print(f"Type: {current_entity_type}")