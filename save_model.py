
import pickle
from train_model import model

# Save the trained machine-learning model
with open("smartlight_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")
print("File created: smartlight_model.pkl")
