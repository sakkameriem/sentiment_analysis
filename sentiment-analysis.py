from transformers import BertTokenizerFast, BertConfig, BertForSequenceClassification

config = BertConfig.from_pretrained("C:/Users/LENOVO/tunbert/models/bert-google/bert/TunBERT_config.json")

model = BertForSequenceClassification.from_pretrained("C:/Users/LENOVO/tunbert/models/bert-google/bert/", config=config)

tokenizer = BertTokenizerFast.from_pretrained("C:/Users/LENOVO/tunbert/models/bert-google/bert", max_len=512)

text = "أسقط بانكة"


tokens = tokenizer(text, return_tensors="tf")


outputs = model(**tokens)
predictions = outputs.logits.argmax(dim=1)


sentiment_label = "positive" if predictions.item() == 1 else "negative"
print(f"Predicted sentiment: {sentiment_label}")
