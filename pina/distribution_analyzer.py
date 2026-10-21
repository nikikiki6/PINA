import numpy as np
import torch
from typing import Dict, List
from transformers import AutoTokenizer, AutoModelForCausalLM
from scipy.stats import entropy

class SimplifiedLogitsAnalyzer:

    def __init__(self, model_path: str='mistralai/Mistral-7B-Instruct-v0.2'):
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            self.model.to(self.device)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
        except Exception as e:
            raise e

    def get_logits(self, text: str) -> np.ndarray:
        system_prompt = "You are a useful assistant. Please answer the questions concisely and informatively. Don't repeat questions! You just need to output the answer."
        messages = [{'role': 'user', 'content': system_prompt}, {'role': 'assistant', 'content': 'Well, I will answer your question as best as I can. Please ask me any questions you may have.'}, {'role': 'user', 'content': text}]
        input_text = self.tokenizer.apply_chat_template(messages, return_tensors='pt')
        input_ids = input_text.to(self.device)
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, return_dict=True)
        return outputs.logits[0].cpu().numpy()

    def get_tokens(self, text: str) -> List[str]:
        system_prompt = "You are a useful assistant. Please answer the questions concisely and informatively. Don't repeat questions! You just need to output the answer."
        messages = [{'role': 'user', 'content': system_prompt}, {'role': 'assistant', 'content': 'Well, I will answer your question as best as I can. Please ask me any questions you may have.'}, {'role': 'user', 'content': text}]
        input_text = self.tokenizer.apply_chat_template(messages, return_tensors='pt')
        tokens = self.tokenizer.convert_ids_to_tokens(input_text[0])
        return tokens

    def calculate_kl_divergence(self, orig_logits: np.ndarray, attack_logits: np.ndarray) -> float:
        orig_probs = torch.softmax(torch.tensor(orig_logits), dim=-1).numpy()
        attack_probs = torch.softmax(torch.tensor(attack_logits), dim=-1).numpy()
        min_len = min(len(orig_probs), len(attack_probs))
        orig_probs = orig_probs[:min_len]
        attack_probs = attack_probs[:min_len]
        kl_divergences = []
        for i in range(min_len):
            kl_div = entropy(attack_probs[i], orig_probs[i])
            kl_divergences.append(kl_div)
        return np.mean(kl_divergences)

    def identify_key_tokens(self, orig_logits: np.ndarray, attack_logits: np.ndarray) -> Dict:
        orig_probs = torch.softmax(torch.tensor(orig_logits), dim=-1).numpy()
        attack_probs = torch.softmax(torch.tensor(attack_logits), dim=-1).numpy()
        min_len = min(len(orig_probs), len(attack_probs))
        orig_probs = orig_probs[:min_len]
        attack_probs = attack_probs[:min_len]
        orig_max_probs = np.max(orig_probs, axis=1)
        attack_max_probs = np.max(attack_probs, axis=1)
        max_prob_changes = attack_max_probs - orig_max_probs
        orig_entropies = np.array([entropy(prob) for prob in orig_probs])
        attack_entropies = np.array([entropy(prob) for prob in attack_probs])
        entropy_changes = attack_entropies - orig_entropies
        significant_changes = []
        for i in range(min_len):
            score = abs(max_prob_changes[i]) + abs(entropy_changes[i])
            if score > 0.1:
                significant_changes.append((i, score, max_prob_changes[i], entropy_changes[i]))
        significant_changes.sort(key=lambda x: x[1], reverse=True)
        return {'significant_changes': significant_changes[:10], 'overall_disruption': np.mean(np.abs(max_prob_changes)) + np.mean(np.abs(entropy_changes))}

    def analyze_attack_effect(self, original_text: str, attack_text: str) -> Dict:
        try:
            orig_logits = self.get_logits(original_text)
            attack_logits = self.get_logits(attack_text)
            orig_tokens = self.get_tokens(original_text)
            attack_tokens = self.get_tokens(attack_text)
            kl_divergence = self.calculate_kl_divergence(orig_logits, attack_logits)
            key_tokens = self.identify_key_tokens(orig_logits, attack_logits)
            analysis = {'original_tokens': orig_tokens, 'attack_tokens': attack_tokens, 'kl_divergence': kl_divergence, 'key_tokens': key_tokens, 'overall_impact': {'prediction_disruption': kl_divergence, 'key_token_impact': key_tokens['overall_disruption'], 'total_impact_score': (kl_divergence + key_tokens['overall_disruption']) / 2}}
            return analysis
        except Exception as e:
            return {'error': str(e), 'overall_impact': {'total_impact_score': 0.0}}
