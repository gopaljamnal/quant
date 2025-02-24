from transformers import pipeline
import torch
import logging
from typing import List, Dict


class NERProcessor:
    def __init__(self,
                 model_name: str = "dbmdz/bert-large-cased-finetuned-conll03-english",
                 confidence_threshold: float = 0.8):
        self.confidence_threshold = confidence_threshold
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.ner_pipeline = pipeline("ner",
                                         model=model_name,
                                         aggregation_strategy="simple",
                                         device=self.device)
        except Exception as e:
            logging.error(f"Failed to initialize NER pipeline: {str(e)}")
            raise

    def process_text(self, text: str) -> List[Dict]:
        if not text or not isinstance(text, str):
            logging.warning("Invalid input text")
            return []

        try:
            # Get predictions
            entities = self.ner_pipeline(text)

            # Post-process results
            filtered_entities = [
                entity for entity in entities
                if entity['score'] >= self.confidence_threshold
            ]

            return filtered_entities
        except Exception as e:
            logging.error(f"Error processing text: {str(e)}")
            return []


if __name__ == "__main__":
    # Initialize processor
    processor = NERProcessor()

    # Text example
    text = """
    Apple Inc. CEO Tim Cook announced new partnerships with Microsoft 
    and Google during a conference in New York City. The event was also 
    attended by Sundar Pichai and Satya Nadella.
    """

    # Process text
    results = processor.process_text(text)

    # Print results
    for entity in results:
        print(f"Entity: {entity['word']}")
        print(f"Type: {entity['entity_group']}")
        print(f"Confidence: {entity['score']:.4f}")
        print("-" * 30)