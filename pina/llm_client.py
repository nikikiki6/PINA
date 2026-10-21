import json
import os
import urllib.request

def chatgpt(sys_prompt, usr_prompt, temperature=0.7, n=1):
    key = os.environ.get('PINA_API_KEY') or os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('PINA_OPTIMIZER_MODEL')
    if not key or not model:
        raise RuntimeError('Set PINA_API_KEY (or OPENAI_API_KEY) and PINA_OPTIMIZER_MODEL')
    base = os.environ.get('PINA_API_BASE', 'https://api.openai.com/v1').rstrip('/')
    body = {'model': model, 'temperature': temperature, 'n': n, 'messages': [{'role': 'system', 'content': sys_prompt}, {'role': 'user', 'content': usr_prompt}]}
    request = urllib.request.Request(base + '/chat/completions', data=json.dumps(body).encode(), headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)
    return [item['message']['content'] for item in result['choices']]
