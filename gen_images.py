import json, base64, urllib.request, urllib.error, os, time

with open(r'C:\Users\Jan Nordskog\norprog\gemini_key.tmp') as f:
    key = f.read().strip()

out_dir = r'C:\Users\Jan Nordskog\norprog\images'

def gen_gemini(prompt, filename):
    model = 'gemini-2.5-flash-image'
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}'
    payload = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'responseModalities': ['TEXT', 'IMAGE'], 'temperature': 0.8}
    }).encode()
    try:
        req = urllib.request.Request(url, data=payload, headers={
            'Content-Type': 'application/json', 'User-Agent': 'ImageGen/1.0'
        })
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read())
        for part in result['candidates'][0]['content']['parts']:
            if 'inlineData' in part:
                img_data = base64.b64decode(part['inlineData']['data'])
                path = os.path.join(out_dir, filename)
                with open(path, 'wb') as f:
                    f.write(img_data)
                print(f'Saved: {filename} ({len(img_data):,} bytes)')
                return True
        print(f'No image data in response: {json.dumps(result)[:300]}')
        return False
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'HTTP Error {e.code}: {body[:400]}')
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False

images = [
    (
        'A photorealistic photograph of a young Scandinavian male web developer in his late 20s '
        'working at a clean modern desk with dual monitors showing code. '
        'Minimalist white Scandinavian office, light oak desk, soft natural window light. '
        'Navy shirt, focused on screen. Shot at 35mm f/2.8. No text, no watermarks.',
        'about-developer.png'
    ),
    (
        'A photorealistic photograph of a professional Norwegian electrician in a yellow hard hat '
        'and dark blue work clothes inspecting an electrical panel. '
        'Clean professional composition. Shot at 50mm f/4.0. No text, no watermarks.',
        'proj-elektro.png'
    ),
    (
        'A photorealistic photograph of a clean modern Scandinavian health clinic reception area. '
        'White interior, green accents, potted plants, warm lighting. No people. '
        'Shot at 35mm f/4.0, architectural style. No text, no watermarks.',
        'proj-klinikk.png'
    ),
    (
        'A photorealistic photograph of a Scandinavian herb and plant shop interior. '
        'Rustic wooden shelves with dried herbs, oils, plant pots. '
        'Warm rose and burgundy lighting, dried flowers hanging from ceiling. '
        'Shot at 35mm f/2.8. No text, no watermarks.',
        'proj-retail.png'
    ),
]

for i, (prompt, filename) in enumerate(images, 1):
    path = os.path.join(out_dir, filename)
    if os.path.exists(path):
        print(f'{i}/{len(images)} Already exists: {filename}, skipping.')
        continue
    print(f'{i}/{len(images)} Generating {filename}...')
    success = gen_gemini(prompt, filename)
    if success and i < len(images):
        print('  Waiting 20s...')
        time.sleep(20)
    elif not success:
        print('  Failed, stopping.')
        break

print('\nDone.')
