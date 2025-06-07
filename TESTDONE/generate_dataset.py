import pandas as pd
import random
from datetime import datetime

# Base templates for generating reviews
positive_templates = [
    "This {product} is amazing! {positive_phrase}",
    "Great {product} with {positive_feature}. {positive_phrase}",
    "Excellent {product}! {positive_phrase}",
    "I love this {product}. {positive_phrase}",
    "Fantastic {product}! {positive_phrase}",
    "Best {product} I've ever used. {positive_phrase}",
    "Outstanding {product}. {positive_phrase}",
    "Wonderful {product}! {positive_phrase}",
    "Superb {product}. {positive_phrase}",
    "Brilliant {product}! {positive_phrase}"
]

neutral_templates = [
    "This {product} is okay. {neutral_phrase}",
    "Decent {product}. {neutral_phrase}",
    "Average {product}. {neutral_phrase}",
    "The {product} is fine. {neutral_phrase}",
    "Not bad {product}. {neutral_phrase}",
    "Acceptable {product}. {neutral_phrase}",
    "Standard {product}. {neutral_phrase}",
    "Regular {product}. {neutral_phrase}",
    "Basic {product}. {neutral_phrase}",
    "Usual {product}. {neutral_phrase}"
]

negative_templates = [
    "This {product} is terrible. {negative_phrase}",
    "Poor quality {product}. {negative_phrase}",
    "Disappointing {product}. {negative_phrase}",
    "Bad {product}. {negative_phrase}",
    "Awful {product}! {negative_phrase}",
    "Horrible {product}. {negative_phrase}",
    "Worst {product} ever. {negative_phrase}",
    "Useless {product}. {negative_phrase}",
    "Waste of money on this {product}. {negative_phrase}",
    "Regret buying this {product}. {negative_phrase}"
]

# Phrases to complete the templates
positive_phrases = [
    "Highly recommended!",
    "Will buy again!",
    "Very satisfied with the purchase.",
    "Worth every penny!",
    "Exceeded my expectations.",
    "Better than expected.",
    "Great value for money.",
    "Perfect for my needs.",
    "Exactly what I wanted.",
    "Couldn't be happier!"
]

neutral_phrases = [
    "Could be better.",
    "Nothing special.",
    "Meets basic requirements.",
    "As expected.",
    "Average quality.",
    "Decent for the price.",
    "Serves its purpose.",
    "Not bad, not great.",
    "Acceptable quality.",
    "Standard features."
]

negative_phrases = [
    "Would not recommend.",
    "Complete waste of money.",
    "Very disappointed.",
    "Not worth the price.",
    "Poor quality.",
    "Terrible experience.",
    "Regret the purchase.",
    "Not as described.",
    "Very misleading.",
    "Stay away from this."
]

# Product categories
products = [
    "smartphone", "laptop", "headphones", "camera", "tablet",
    "smartwatch", "printer", "monitor", "keyboard", "mouse",
    "speaker", "router", "powerbank", "charger", "cable",
    "earphones", "microphone", "webcam", "hard drive", "memory card"
]

# Features for positive reviews
positive_features = [
    "excellent build quality",
    "amazing performance",
    "great battery life",
    "beautiful design",
    "fast processing",
    "crystal clear display",
    "comfortable to use",
    "reliable performance",
    "innovative features",
    "premium feel"
]

def generate_review():
    sentiment = random.choice(['positive', 'neutral', 'negative'])
    
    if sentiment == 'positive':
        template = random.choice(positive_templates)
        phrase = random.choice(positive_phrases)
        feature = random.choice(positive_features)
    elif sentiment == 'neutral':
        template = random.choice(neutral_templates)
        phrase = random.choice(neutral_phrases)
        feature = "basic features"
    else:
        template = random.choice(negative_templates)
        phrase = random.choice(negative_phrases)
        feature = "poor quality"
    
    product = random.choice(products)
    
    review = template.format(
        product=product,
        positive_feature=feature,
        positive_phrase=phrase,
        neutral_phrase=phrase,
        negative_phrase=phrase
    )
    
    return review, sentiment

# Generate 5000 reviews
reviews = []
sentiments = []

for _ in range(5000):
    review, sentiment = generate_review()
    reviews.append(review)
    sentiments.append(sentiment)

# Create DataFrame
df = pd.DataFrame({
    'review_text': reviews,
    'sentiment': sentiments
})

# Save to CSV
df.to_csv('large_dataset.csv', index=False)
print(f"Generated dataset with {len(df)} reviews")
print("\nSentiment distribution:")
print(df['sentiment'].value_counts()) 