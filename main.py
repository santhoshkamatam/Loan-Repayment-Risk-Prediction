import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_preprocessing import DataPreprocessor
from src.model import LoanRiskModel
from src.evaluation import evaluate_model


# BUSINESS RULE OVERRIDE
def apply_credit_score_rule(X, y_pred, feature_names, threshold=650):
    """
    Rule-based override:
    If Credit Score < threshold -> High Risk (1)
    """
    if 'credit_score' not in feature_names:
        print(" Warning: 'credit_score' feature not found. Rule not applied.")
        return y_pred

    credit_score_idx = feature_names.index('credit_score')

    y_pred_rule = y_pred.copy()
    low_score_mask = X[:, credit_score_idx] < threshold

    # 1 = High Risk, 0 = Low Risk
    y_pred_rule[low_score_mask] = 1

    return y_pred_rule


def train_pipeline(data_path: str, output_dir: str = 'models'):

    print("\n" + "=" * 70)
    print(" LOAN REPAYMENT RISK PREDICTION - TRAINING PIPELINE")
    print("=" * 70)

    # Initialize components
    preprocessor = DataPreprocessor()
    model = LoanRiskModel()

    # STEP 1: Data Loading
    print("\n STEP 1: Loading Data")
    print("-" * 50)
    df = preprocessor.load_data(data_path)

    stats = preprocessor.explore_data(df)
    print(f"   Dataset shape: {stats['shape']}")
    print(f"   Target distribution: {stats['target_distribution']}")

    # STEP 2: Data Cleaning
    print("\n STEP 2: Data Cleaning")
    print("-" * 50)
    df_clean = preprocessor.clean_data(df)

    # STEP 3: Feature Engineering
    print("\n STEP 3: Feature Engineering")
    print("-" * 50)
    df_featured = preprocessor.create_features(df_clean)

    # STEP 4: Feature Preparation & Scaling
    print("\n STEP 4: Feature Preparation & Scaling")
    print("-" * 50)
    X, y, feature_names = preprocessor.prepare_features(
        df_featured, fit_scaler=True
    )
    print(f"   Total features: {len(feature_names)}")
    print(f"   Features: {feature_names}")

    # STEP 5: Train-Test Split
    print("\n STEP 5: Train-Test Split")
    print("-" * 50)
    X_train, X_test, y_train, y_test = preprocessor.split_data(
        X, y, test_size=0.2
    )

    # STEP 6: Model Training
    print("\n STEP 6: Model Training")
    print("-" * 50)
    model.train(X_train, y_train, feature_names)

    # Cross-validation
    model.cross_validate(X, y, cv=5)

    # STEP 7: Model Evaluation
    print("\n STEP 7: Model Evaluation")
    print("-" * 50)

    # Model predictions
    y_pred_model = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    # Apply Credit Score rule
    y_pred = apply_credit_score_rule(
        X_test,
        y_pred_model,
        feature_names,
        threshold=650
    )

    overrides = (y_pred != y_pred_model).sum()
    print(f"   Rule-based overrides applied: {overrides}")

    # Feature importance
    feature_importance = model.get_feature_importance()

    # Evaluation metrics
    metrics = evaluate_model(
        y_test,
        y_pred,
        y_proba,
        feature_importance,
        output_dir='outputs'
    )

    # STEP 8: Save Artifacts
    print("\n STEP 8: Saving Model Artifacts")
    print("-" * 50)

    os.makedirs(output_dir, exist_ok=True)

    model.save(os.path.join(output_dir, 'loan_risk_model.pkl'))
    preprocessor.save_scaler(os.path.join(output_dir, 'scaler.pkl'))

    print("\n" + "=" * 70)
    print(" TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"""
     Final Results:
       • Accuracy:  {metrics['accuracy']:.4f}
       • Precision: {metrics['precision']:.4f}
       • Recall:    {metrics['recall']:.4f}
       • F1-Score:  {metrics['f1_score']:.4f}
       • ROC-AUC:   {metrics.get('roc_auc', 'N/A'):.4f}

     Business Rule:
       • Credit Score < 650 → High Risk (Forced)

     Saved Files:
       • Model:     {output_dir}/loan_risk_model.pkl
       • Scaler:    {output_dir}/scaler.pkl
       • Plots:     outputs/

     Next Steps:
       • Run 'streamlit run app.py'
       • Open notebooks/Loan_Risk_Analysis.ipynb
    """)

    return model, preprocessor, metrics


if __name__ == "__main__":
    data_path = 'loan_repayment_risk_30000.csv'

    if len(sys.argv) > 1:
        data_path = sys.argv[1]

    if not os.path.exists(data_path):
        print(f" Error: Data file not found: {data_path}")
        sys.exit(1)

    model, preprocessor, metrics = train_pipeline(data_path)
