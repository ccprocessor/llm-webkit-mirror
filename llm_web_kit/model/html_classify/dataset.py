from torch.utils.data import Dataset


class MarkupLMDataset(Dataset):
    def __init__(self, html_strings, processor):
        self.html_strings = html_strings  # Store raw strings
        self.processor = processor  # Store processor for later use
        self.max_length = 512  # Add a max length parameter (adjust as needed)

    def __getitem__(self, idx):
        encoding = self.processor(
            self.html_strings[idx],
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=self.max_length
        )
        # Remove batch dimension added by processor
        item = {key: val.squeeze(0) for key, val in encoding.items()}
        return item

    def __len__(self):
        return len(self.html_strings)
