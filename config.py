### arxiv-search.py
restrict_to_most_recent = True
max_results = 5000
categories = "cat:cs.AI OR cat:stat.ML OR cat:cs.CL OR cat:cs.LG OR cat:cs.MA OR cat:cs.MA"

### generate_newsletter.py 
# Mess around with these prompts to tease out specific information you're looking for
prompts = [ # don't forget commas if you add more prompts to the list
"You are an expert scientific researcher speaking to a somewhat technical audience. Please provide clear, concise descriptions and explanations of the core assertions, methodology, results, potential critiques of, and/or implications elucidated herein, if any. Specificity is preferred over broad or vague statements. Be very concise; write dense, meaningful sentences with minimal word fluff."#,
#"You are an expert scientific researcher with a wide range of cross-disciplinary background knowledge. List all of the prerequisite knowledge required in order to understand the concepts laid out here. Please answer extremely concisely in a simple bulleted format. Entries should include both individual concepts as well as the names of disciplines and sub-disciplines. Also, please provide a complete citation for this paper to the best of your ability given the information provided. Only include a url if it is listed in the content of the paper." 
]

### cleanup.py
# Change to False if you don't use obsidian
send_to_obsidian = True
# vault_location is wherever you want the .md summaries to go, and attachments_location is wherever you want the pdf files to go
# For people who use obsidian 'correctly' this might be the exact same folder
obsidian_vault_location = '/Users/tunadorable/Vault' #'your/obsidian/vault/location/here'
obsidian_vault_attachments_location = '/Users/tunadorable/Vault/attachments' #'your/obsidian/vault/location/here/attachments-folder'
# lines to add to the beginning of each summary.md file in obsidian. I've left mine in as examples
frontmatter_lines = '#pdf\n#needsNote\n#needsVideo\n#unread\n'

### timestamps.py
# The hotkey used to start the next yt chapter (`esc` ends the process)
hotkey = '`'
# the strings to replace with shorter versions
replacements = {
    "Multimodal Large Language Model": "MLLM",
    "Large Language Model": "LLM",
    "large language model": "LLM",
    "language model": "LM",
    "Language Model": "LM",
    "Mixture-of-Experts": "MoE",
    "Mixture of Experts": "MoE",
    "Artificial Neural Network": "ANN",
    "Deep Neural Network": "DNN",
    "Graph Neural Network": "GNN",
    "Neural Network": "NN",
    "Monte Carlo Tree Search": "MCTS",
    "Monte Carlo": "MC",
    "Reinforcement Learning with Human Feedback": "RLHF",
    "Direct Preference Optimization": "DPO",
    "Preference Optimization": "PO",
    "Natural Language Processing": "NLP",
    "Natural Language": "NL",
    "Convolutional Neural Network": "CNN",
    "Generative Adversarial Network": "GAN",
    "Graph Neural Network": "GNN",
    "Long Short-Term Memory": "LSTM",
    "Support Vector Machine": "SVM",
    "Principal Component Analysis": "PCA",
    "Stochastic Gradient Descent": "SGD",
    "Transformer Model": "Transformer",
    "Attention Mechanism": "Attention",
    "Self-Attention Mechanism": "Self-Attention",
    "Bidirectional Encoder Representations from Transformers": "BERT",
    "Recursive Neural Network": "RNN",
    "Autoregressive Model": "AR Model",
    "Machine Learning": "ML",
    "Artificial Intelligence": "AI",
    "Reinforcement Learning": "RL",
    "Explainable AI": "XAI",
    "Federated Learning": "FL",
    "K-Nearest Neighbors": "KNN",
    "Markov Decision Process": "MDP",
    "Variational Autoencoder": "VAE",
    "Autoencoder": "AE",
    "Singular Value Decomposition": "SVD",
    "Continual Learning": "CL",
    "Chain of Thought": "CoT",
    "Chains of Thought": "CoTs",
    "State Space Model": "SSM",
    "state space model": "SSM",
}
# the lines will be trimmed away until they get below this character count. 
limit = 4475
    # papers that i spent less time on get trimmed first
