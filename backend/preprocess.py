import re

def compute_edit_distance(word1: str, word2: str) -> int:
    """Computes Levenshtein distance between two words."""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],       # Remove
                                   dp[i][j-1],       # Insert
                                   dp[i-1][j-1])     # Replace
    return dp[m][n]

class NLPPreprocessor:
    def __init__(self):
        # A dictionary for demonstration of Edit Distance based spellcheck.
        self.vocabulary = {
            "happy": "happy", "sad": "sad", "angry": "angry", 
            "scared": "scared", "terrified": "terrified",
            "furious": "furious", "love": "love", "amazed": "amazed",
            "now": "now", "so": "so", "dark": "dark", "shocked": "shocked",
            "sudden": "sudden", "news": "news", "heart": "heart",
            "tragic": "tragic", "family": "family", "lovely": "lovely"
        }

    def normalize_text(self, text: str) -> str:
        """Applies Regular Expressions to normalize the text."""
        # 1. Lowercase
        text = text.lower()
        # 2. Remove multiple exclamation/question marks (e.g., "!!!" -> "!")
        text = re.sub(r'([!?.]){2,}', r'\1', text)
        # 3. Reduce exaggerated repeated letters (e.g., "soooo" -> "so")
        text = re.sub(r'(.)\1{2,}', r'\1', text)
        return text

    def spell_check(self, text: str, max_distance: int = 1) -> str:
        """Applies Edit Distance to correct common misspellings from our vocabulary."""
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Strip punctuation momentarily for spell check
            clean_word = re.sub(r'[^\w\s]', '', word)
            best_match = word
            
            # Only attempt to spell correct if word is significant length
            if clean_word and len(clean_word) > 3 and clean_word not in self.vocabulary:
                min_dist = max_distance + 1
                for vocab_word in self.vocabulary:
                    dist = compute_edit_distance(clean_word, vocab_word)
                    if dist < min_dist and dist <= max_distance:
                        min_dist = dist
                        best_match = word.replace(clean_word, vocab_word) # Retain original punctuation
                        
            corrected_words.append(best_match)
            
        return " ".join(corrected_words)

    def process(self, text: str) -> dict:
        """Full pipeline: Normalization -> Spell Check."""
        normalized = self.normalize_text(text)
        checked = self.spell_check(normalized)
        return {
            "original": text,
            "processed": checked
        }
