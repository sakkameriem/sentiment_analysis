from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("AhmedBou/TuniBert")
model = AutoModelForSequenceClassification.from_pretrained("AhmedBou/TuniBert")

batch_size = 1000
input_file = 'Zitouna data.csv'
output_file = 'Zitouna data labeled.csv'

data_reader = pd.read_csv(input_file, chunksize=batch_size)

results = pd.DataFrame(columns=["text", "logits", "label"])
for chunk in data_reader:
    batch_results = pd.DataFrame(columns=["text", "logits", "label"])
    for i, row in chunk.iterrows():
        text = row['text']
        tokens = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model(**tokens)
        logits = outputs.logits.detach().numpy()
        predictions = np.argmax(logits, axis=1)
        sentiment_label = "neutral" if predictions[0] == 0 else "positive" if predictions[0] == 1 else "negative"

        new_row = pd.DataFrame({
            "text": [text],
            "logits": [logits.tolist()],
            "label": [sentiment_label]
        })

        for col in chunk.columns:
            if col != 'text':
                new_row[col] = row[col]

        batch_results = pd.concat([batch_results, new_row], ignore_index=True)

    results = pd.concat([results, batch_results], ignore_index=True)

display(results.head(20))
results.to_csv(output_file, index=False)