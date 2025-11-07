# PINA: PROMPT INJECTION ATTACK AGAINST NAVIGATION AGENTS

---

### Abstract 

Navigation agents powered by large language models (LLMs) convert natural language instructions into executable plans and actions. Compared to text-based applications, their security is far more critical: a successful prompt injection attack does not just alter outputs but can directly misguide physical navigation, leading to unsafe routes, mission failure, or real-world harm. Despite this high-stakes setting, the vulnerability of navigation agents to prompt injection remains largely unexplored. In this paper, we propose PINA, an adaptive prompt optimization framework tailored to navigation agents under black-box, long-context, and action-executable constraints. Experiments on indoor and outdoor navigation agents show that PINA achieves high attack success rates with an average ASR of 87.5%, surpasses all baselines, and remains robust under ablation and adaptive-attack conditions.
This work provides the first systematic investigation of prompt injection attacks in navigation and highlights their urgent security implications for embodied LLM agents.

---

### Method
<img width="747" height="227" alt="image" src="https://github.com/user-attachments/assets/cb2764b3-7951-433d-bfc4-50c9d7601d65" />
By integrating an (1) Attack Evaluator, which quantifies impact using navigation metrics, and a (2)
Distribution Analyzer, which captures global KL divergence and local key tokens, into an (3) Adaptive Refinement loop, PINA
iteratively updates injection prompts, enabling effective black-box attacks on navigation agents.

---

### Code

Code will be released upon paper acceptance.


