import spacy
from spacy.pipeline.textcat import Config, single_label_cnn_config
from spacy.training import Example
import random
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_recall_fscore_support, classification_report

import json

def load_training_data_grouped_from_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        grouped_data = json.load(f)

    labels = list(grouped_data.keys())
    formatted_data = []

    for label, texts in grouped_data.items():
        for text in texts:
            cats = {l: 1.0 if l == label else 0.0 for l in labels}
            formatted_data.append((text, {"cats": cats}))
    
    return formatted_data, labels

TRAINING_DATA, labels = load_training_data_grouped_from_json("training_data_grouped.json")

# Load blank English model
nlp = spacy.blank("en")

# Add text categorizer pipeline
textcat = nlp.add_pipe("textcat", last=True)

# Add labels
# Add labels dynamically
for label in labels:
    textcat.add_label(label)

# Train the model
def train_model(nlp, data, epochs=100, patience=10):  
    optimizer = nlp.begin_training()
    best_loss = float('inf')  
    epochs_without_improvement = 0  

    for epoch in range(epochs):
        random.shuffle(data)
        losses = {}
        
        for text, annotations in data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, losses=losses)
        
        current_loss = losses.get("textcat", float('inf'))
        print(f"Epoch {epoch+1}, Loss: {current_loss}")
        
        if current_loss < best_loss:
            best_loss = current_loss
            epochs_without_improvement = 0  
        else:
            epochs_without_improvement += 1  

        if epochs_without_improvement >= patience:  
            print(f"Stopping early at epoch {epoch+1} due to no improvement for {patience} epochs.")
            break  

train_model(nlp, TRAINING_DATA)

# Save the model
nlp.to_disk("intent_model")

# Load and test the model
nlp_test = spacy.load("intent_model")

def classify_intent(text):
    doc = nlp_test(text)
    return max(doc.cats, key=doc.cats.get) if doc.cats else "other"



# Test data
test_texts = [


    ("mark star neetcode by this monday done.", "complete_task"),
    ("cancel 67", "delete_task"),
    ("mark 67 done", "complete_task"),
    ("mark 6 completed", "complete_task"),
    ("delete 6", "delete_task"),
    ("cancel 67", "delete_task"),
    ("1 finished", "complete_task"),
    ("icecrea", "other"),
    ("cry", "other"),
    ("😇", "other"),
    ("😚😚", "other"),
    ("🤓", "other"),
    ("😕", "other"),
    ("😊", "other"),
    ("😋", "other")



]

# Make predictions
y_true = []
y_pred = []
misclassified = []  # Store misclassified examples
predicted_counts = {}

for text, actual_label in test_texts:
    predicted_label = classify_intent(text)  # Your existing function
    y_true.append(actual_label)
    y_pred.append(predicted_label)
    print(f"Input: {text} → Predicted: {predicted_label}, Actual: {actual_label}")
    
    # Count how many times each label is predicted
    predicted_counts[predicted_label] = predicted_counts.get(predicted_label, 0) + 1

    # Check for misclassification
    if predicted_label != actual_label:
        misclassified.append((text, actual_label, predicted_label))

# Compute Precision, Recall, and F1 Score
precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=1)

# Print classification report
print("\n🔍 **Evaluation Metrics:**")
print(f"✅ Precision: {precision:.2f}")
print(f"✅ Recall: {recall:.2f}")
print(f"✅ F1 Score: {f1:.2f}")

# Show label count distribution
print(f"📊 Predicted Labels Count: {predicted_counts}")

# Show misclassified examples
if misclassified:
    print("\n❌ **Misclassified Examples:**")
    for text, actual, predicted in misclassified:
        print(f"🔴 Input: '{text}' → Predicted: {predicted}, Actual: {actual}")
else:
    print("\n✅ No misclassifications! The model performed perfectly.")