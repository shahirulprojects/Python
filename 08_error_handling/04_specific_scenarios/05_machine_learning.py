# error handling in machine learning operations
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
import pandas as pd
from typing import Any, Dict, List, Optional, Union, Tuple
import logging
import joblib
from pathlib import Path
import json
from dataclasses import dataclass
import torch
from torch.utils.data import Dataset, DataLoader
import tensorflow as tf

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# custom exceptions
class MLError(Exception):
    """base class for machine learning errors."""
    pass

class DataError(MLError):
    """error for data-related issues."""
    pass

class ModelError(MLError):
    """error for model-related issues."""
    pass

class PredictionError(MLError):
    """error for prediction-related issues."""
    pass

@dataclass
class ModelMetadata:
    """metadata for ML models."""
    name: str
    version: str
    features: List[str]
    target: str
    metrics: Dict[str, float]
    timestamp: str

class DataValidator:
    """validate ML data."""
    
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
    
    def validate(self, data: pd.DataFrame) -> None:
        """validate dataframe against schema."""
        try:
            # check required columns
            missing_cols = set(self.schema['features']) - set(data.columns)
            if missing_cols:
                raise DataError(f"missing columns: {missing_cols}")
            
            # check data types
            for col, dtype in self.schema['dtypes'].items():
                if col in data.columns and not pd.api.types.is_dtype_equal(
                    data[col].dtype, dtype
                ):
                    raise DataError(
                        f"column '{col}' has wrong type: "
                        f"expected {dtype}, got {data[col].dtype}"
                    )
            
            # check value ranges
            for col, range_info in self.schema.get('ranges', {}).items():
                if col in data.columns:
                    min_val, max_val = range_info
                    if data[col].min() < min_val or data[col].max() > max_val:
                        raise DataError(
                            f"column '{col}' has values outside range "
                            f"[{min_val}, {max_val}]"
                        )
            
            # check for nulls
            if not self.schema.get('allow_nulls', False):
                null_cols = data.columns[data.isnull().any()].tolist()
                if null_cols:
                    raise DataError(f"null values found in columns: {null_cols}")
        
        except Exception as e:
            if not isinstance(e, DataError):
                raise DataError(f"data validation failed: {str(e)}")
            raise

class ModelManager:
    """manage ML models with error handling."""
    
    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def save_model(self, model: BaseEstimator, metadata: ModelMetadata) -> None:
        """save model with metadata."""
        try:
            # save model
            model_path = self.model_dir / f"{metadata.name}_{metadata.version}.joblib"
            joblib.dump(model, model_path)
            
            # save metadata
            meta_path = model_path.with_suffix('.json')
            with open(meta_path, 'w') as f:
                json.dump(metadata.__dict__, f, indent=2)
        
        except Exception as e:
            raise ModelError(f"failed to save model: {str(e)}")
    
    def load_model(self, name: str, version: str) -> Tuple[BaseEstimator, ModelMetadata]:
        """load model and metadata."""
        try:
            # load model
            model_path = self.model_dir / f"{name}_{version}.joblib"
            if not model_path.exists():
                raise ModelError(f"model not found: {model_path}")
            
            model = joblib.load(model_path)
            
            # load metadata
            meta_path = model_path.with_suffix('.json')
            if not meta_path.exists():
                raise ModelError(f"metadata not found: {meta_path}")
            
            with open(meta_path, 'r') as f:
                metadata = ModelMetadata(**json.load(f))
            
            return model, metadata
        
        except Exception as e:
            if not isinstance(e, ModelError):
                raise ModelError(f"failed to load model: {str(e)}")
            raise

class PredictionService:
    """service for making predictions with error handling."""
    
    def __init__(self, model: BaseEstimator, metadata: ModelMetadata):
        self.model = model
        self.metadata = metadata
        self.validator = DataValidator({
            'features': metadata.features,
            'dtypes': {f: 'float64' for f in metadata.features},
            'allow_nulls': False
        })
    
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """make predictions with error handling."""
        try:
            # validate input data
            self.validator.validate(data)
            
            # check if model is fitted
            if not hasattr(self.model, 'predict'):
                raise ModelError("model does not support predictions")
            
            # make predictions
            predictions = self.model.predict(data[self.metadata.features])
            return predictions
        
        except (DataError, ModelError):
            raise
        except Exception as e:
            raise PredictionError(f"prediction failed: {str(e)}")

# PyTorch error handling
class SafeDataset(Dataset):
    """dataset with error handling."""
    
    def __init__(self, data: np.ndarray, targets: np.ndarray):
        if len(data) != len(targets):
            raise DataError(
                f"data and targets have different lengths: "
                f"{len(data)} vs {len(targets)}"
            )
        
        self.data = torch.FloatTensor(data)
        self.targets = torch.FloatTensor(targets)
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        try:
            return self.data[idx], self.targets[idx]
        except Exception as e:
            raise DataError(f"failed to get item at index {idx}: {str(e)}")

class SafeModel(torch.nn.Module):
    """neural network with error handling."""
    
    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.layer1 = torch.nn.Linear(input_size, hidden_size)
        self.layer2 = torch.nn.Linear(hidden_size, output_size)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        try:
            x = torch.relu(self.layer1(x))
            return self.layer2(x)
        except Exception as e:
            raise ModelError(f"forward pass failed: {str(e)}")

# TensorFlow error handling
class TFModelWrapper:
    """wrapper for TensorFlow models with error handling."""
    
    def __init__(self, model: tf.keras.Model):
        self.model = model
    
    def safe_predict(self, data: np.ndarray) -> np.ndarray:
        """make predictions with error handling."""
        try:
            # validate input shape
            expected_shape = self.model.input_shape[1:]
            if data.shape[1:] != expected_shape:
                raise DataError(
                    f"invalid input shape: expected {expected_shape}, "
                    f"got {data.shape[1:]}"
                )
            
            # make predictions
            return self.model.predict(data)
        
        except tf.errors.OpError as e:
            raise ModelError(f"TensorFlow operation failed: {str(e)}")
        except Exception as e:
            if not isinstance(e, (DataError, ModelError)):
                raise PredictionError(f"prediction failed: {str(e)}")
            raise

# example usage
def main():
    """demonstrate ML error handling."""
    # 1. data validation
    print("1. testing data validation:")
    try:
        schema = {
            'features': ['x1', 'x2'],
            'dtypes': {'x1': 'float64', 'x2': 'float64'},
            'ranges': {'x1': (-1, 1), 'x2': (-1, 1)},
            'allow_nulls': False
        }
        
        validator = DataValidator(schema)
        
        # invalid data
        data = pd.DataFrame({
            'x1': [1, 2, None],  # contains null
            'x2': ['a', 'b', 'c']  # wrong type
        })
        
        validator.validate(data)
    except DataError as e:
        print(f"data error: {e}")
    
    # 2. model management
    print("\n2. testing model management:")
    try:
        # create dummy model and metadata
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        metadata = ModelMetadata(
            name='linear_model',
            version='1.0.0',
            features=['x1', 'x2'],
            target='y',
            metrics={'r2': 0.95},
            timestamp='2024-01-01'
        )
        
        # save and load model
        manager = ModelManager('models')
        manager.save_model(model, metadata)
        
        loaded_model, loaded_metadata = manager.load_model(
            'linear_model', '1.0.0'
        )
        print(f"loaded model metadata: {loaded_metadata}")
    except ModelError as e:
        print(f"model error: {e}")
    
    # 3. prediction service
    print("\n3. testing prediction service:")
    try:
        service = PredictionService(loaded_model, loaded_metadata)
        
        # invalid prediction data
        data = pd.DataFrame({
            'x1': [1, 2, 3],
            'wrong_feature': [4, 5, 6]
        })
        
        predictions = service.predict(data)
    except (DataError, PredictionError) as e:
        print(f"prediction error: {e}")
    
    # 4. PyTorch error handling
    print("\n4. testing PyTorch error handling:")
    try:
        # create dataset with mismatched data
        data = np.random.randn(10, 5)
        targets = np.random.randn(8)  # wrong length
        
        dataset = SafeDataset(data, targets)
    except DataError as e:
        print(f"PyTorch data error: {e}")
    
    # 5. TensorFlow error handling
    print("\n5. testing TensorFlow error handling:")
    try:
        # create model expecting specific input shape
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, input_shape=(5,)),
            tf.keras.layers.Dense(1)
        ])
        
        wrapper = TFModelWrapper(model)
        
        # wrong input shape
        data = np.random.randn(3, 10)  # should be (batch_size, 5)
        predictions = wrapper.safe_predict(data)
    except (DataError, ModelError) as e:
        print(f"TensorFlow error: {e}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a model monitoring system that:
#    - tracks prediction quality
#    - detects data drift
#    - handles model degradation
#    - triggers retraining

# 2. create a model serving system that:
#    - handles multiple model versions
#    - implements A/B testing
#    - provides prediction caching
#    - monitors performance

# 3. create a training pipeline that:
#    - validates training data
#    - handles training failures
#    - implements early stopping
#    - saves checkpoints 