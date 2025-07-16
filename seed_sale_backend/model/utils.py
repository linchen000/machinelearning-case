import joblib


def save_model(best_model, filename='best_model.pkl'):
    """
    Save the trained model to a pickle file
    
    Args:
        best_model: The trained model to save
        filename: Name of the file to save the model to
    """
    joblib.dump(best_model, filename)
    print(f"Model saved to {filename}")


def load_model(filename='best_model.pkl'):
    """
    Load a trained model from a pickle file
    
    Args:
        filename: Name of the file to load the model from
        
    Returns:
        The loaded model
    """
    model = joblib.load(filename)
    print(f"Model loaded from {filename}")
    return model