import os
from typing import Dict, List, Union

import torch

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.logger import mylogger as logger
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              get_unzip_dir,
                                              import_transformer,
                                              unzip_local_file)


class E5ScoreModel:
    """Mathematical content detection model using E5 embeddings and
    classification."""

    def __init__(self, model_path: str = None, config: Dict = None) -> None:
        """Initialize the E5ScoreModel.

        Args:
            model_path: Path to the model directory. If None, will auto-download.
            config: Configuration dictionary with model parameters.
        """
        if not model_path:
            model_path = self.auto_download()

        # Load configuration from config parameter or default values
        config = config or {}

        self.model_name = config.get('model_name', 'HuggingFaceTB/finemath-classifier')
        self.max_tokens = config.get('max_tokens', 512)
        self.batch_size = config.get('batch_size', 32)
        self.use_flash_attn = config.get('use_flash_attn', False)
        self.device = config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')

        # Import transformers module
        transformers_module = import_transformer()

        # Load model and tokenizer
        logger.info(f'Loading math detection model: {self.model_name}')

        # Configure model loading parameters based on device
        model_kwargs = {
            'trust_remote_code': True
        }

        if self.device == 'cuda' and torch.cuda.is_available():
            try:
                # Try to use GPU with accelerate if available
                model_kwargs.update({
                    'torch_dtype': torch.float16,
                    'device_map': 'auto'
                })
                self.model = transformers_module.AutoModelForSequenceClassification.from_pretrained(
                    self.model_name, **model_kwargs
                )
            except ImportError:
                # Fallback to CPU if accelerate is not available
                logger.warning('Accelerate not available, falling back to CPU')
                self.device = 'cpu'
                model_kwargs = {'trust_remote_code': True}
                self.model = transformers_module.AutoModelForSequenceClassification.from_pretrained(
                    self.model_name, **model_kwargs
                )
        else:
            # Use CPU
            self.model = transformers_module.AutoModelForSequenceClassification.from_pretrained(
                self.model_name, **model_kwargs
            )

        self.tokenizer = transformers_module.AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        # Set model to evaluation mode and move to device
        self.model.eval()
        if self.device == 'cuda':
            self.model.to(self.device, dtype=torch.float16)
        else:
            self.model.to(self.device)

        # Configure tokenizer settings to match HuggingFace documentation pattern
        self.tokenizer_config = {
            'padding': 'longest',
            'truncation': True,
            'max_length': self.max_tokens,
            'return_tensors': 'pt'
        }

        # Output configuration
        self.output_prefix = ''
        self.output_postfix = ''

        logger.info(f'Math detection model loaded successfully on {self.device}')

    def auto_download(self) -> str:
        """Auto-download math detection model resources.

        Returns:
            Path to the downloaded and extracted model directory.
        """
        resource_name = 'math_detector_25m7'
        try:
            resource_config = load_config()['resources']
            math_config: Dict = resource_config[resource_name]
            math_s3 = math_config['download_path']
            math_md5 = math_config.get('md5', '')

            # Get the zip path calculated by the s3 path
            zip_path = os.path.join(CACHE_DIR, f'{resource_name}.zip')
            # The unzip path is calculated by the zip path
            unzip_path = get_unzip_dir(zip_path)
            logger.info(f'Try to make unzip_path: {unzip_path}')

            # If the unzip path does not exist, download the zip file and unzip it
            if not os.path.exists(unzip_path):
                logger.info(f'unzip_path: {unzip_path} does not exist')
                logger.info(f'Try to unzip from zip_path: {zip_path}')
                if not os.path.exists(zip_path):
                    logger.info(f'zip_path: {zip_path} does not exist')
                    logger.info(f'Downloading {math_s3}')
                    zip_path = download_auto_file(math_s3, zip_path, math_md5)
                logger.info(f'Unzipping {zip_path}')
                unzip_path = unzip_local_file(zip_path, unzip_path)
            else:
                logger.info(f'unzip_path: {unzip_path} exists')
            return unzip_path
        except Exception as e:
            logger.warning(f'Failed to auto-download math detector model: {e}')
            logger.info('Using HuggingFace model directly')
            return None

    def get_output_key(self, key: str) -> str:
        """Generate output key with prefix and postfix."""
        if self.output_prefix:
            key = f'{self.output_prefix}_{key}'
        if self.output_postfix:
            key = f'{key}_{self.output_postfix}'
        return key

    def predict(self, texts: Union[List[str], str]) -> List[Dict]:
        """Predict mathematical content scores for input texts.

        Args:
            texts: Input text(s) to analyze for mathematical content.

        Returns:
            List of dictionaries containing score and int_score for each input.
        """
        # Convert single text to list for consistent processing
        if isinstance(texts, str):
            texts = [texts]

        # Tokenize inputs using the exact pattern from HuggingFace documentation
        inputs = self.tokenizer(texts, return_tensors='pt', padding='longest', truncation=True)

        # Move inputs to device if using CUDA
        if self.device == 'cuda':
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            # Get model predictions
            outputs = self.model(**inputs)
            logits = outputs.logits.squeeze(-1).float().detach()

            # Convert to numpy for processing
            scores = logits.cpu().numpy()

        # Format outputs following the exact pattern from requirements
        results = []
        for i, score in enumerate(scores):
            score_float = float(score)
            int_score = int(round(max(0, min(score_float, 5))))  # Clamp to 0-5 range

            result = {
                'text': texts[i],
                'score': score_float,
                'int_score': int_score,
            }

            # Also include the output keys for compatibility with existing interface
            output = {
                self.get_output_key('score'): score_float,
                self.get_output_key('int_score'): int_score
            }
            output.update(result)  # Include both formats for compatibility
            results.append(output)

        return results
