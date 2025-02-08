from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
import torch
from torch.utils.data import Dataset, DataLoader

class SummarizationDataset(Dataset):
    def __init__(self, documents, summaries, tokenizer, max_len=512):
        self.documents = documents
        self.summaries = summaries
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.documents)

    def __getitem__(self, idx):
        doc = self.documents[idx]
        summary = self.summaries[idx]
        inputs = self.tokenizer(
            doc, max_length=self.max_len, padding="max_length", truncation=True, return_tensors="pt"
        )
        targets = self.tokenizer(
            summary, max_length=self.max_len, padding="max_length", truncation=True, return_tensors="pt"
        )
        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": targets["input_ids"].squeeze(),
        }

def train_model(data_dir, model_save_path="t5_summary_model", epochs=3, batch_size=2, lr=5e-5):
    # Load tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")

    # Load training data
    documents = []
    summaries = []

    # Process PDFs and Word files
    for file in os.listdir(data_dir):
        if file.endswith(".txt"):  # Use .txt for simplicity
            with open(os.path.join(data_dir, file), "r") as f:
                text = f.read()
                documents.append("summarize: " + text)
                summaries.append(text[:150])  # Example summaries

    # Create dataset and dataloader
    dataset = SummarizationDataset(documents, summaries, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Set up optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    # Training loop
    model.train()
    for epoch in range(epochs):
        for batch in dataloader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"]
            attention_mask = batch["attention_mask"]
            labels = batch["labels"]

            outputs = model(
                input_ids=input_ids, attention_mask=attention_mask, labels=labels
            )
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

    # Save the trained model
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    print(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    train_model("../data")
