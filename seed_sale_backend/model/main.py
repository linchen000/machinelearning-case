"""
Main script to run the ML Pipeline
"""

from model_pipeline import ModelPipeline
from utils import save_model


def main():
    """
    Main function to run the complete ML pipeline
    """
    print("=" * 50)
    print("Starting ML Pipeline")
    print("=" * 50)
    
    # Initialize the pipeline
    pipeline = ModelPipeline()
    
    # Train the model
    print("\n--- Training Phase ---")
    best_model = pipeline.fit()
    
    # Save the trained model
    save_model(best_model, './best_model.pkl')
    
    # Make predictions on test data
    print("\n--- Prediction Phase ---")
    predictions = pipeline.score()
    
    print("=" * 50)
    print("Pipeline completed successfully!")
    print(f"Final predictions: {predictions}")
    print("=" * 50)


if __name__ == "__main__":
    main()