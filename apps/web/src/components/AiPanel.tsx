'use client';

// Client island: AI assistant panel. Port of build_site.py:261-493.
// Two modes:
//  1. Copy-to-chat — copies a prompt to clipboard and opens claude.ai / chatgpt / deepseek.
//  2. BYOK direct — sends the prompt directly to OpenAI / DeepSeek / Mistral with the
//     user's own API key (stored in localStorage). No Anthropic-direct (no CORS).

import { useEffect, useRef, useState } from 'react';

type Service = 'claude' | 'gpt' | 'deepseek';
type Provider = 'openai' | 'deepseek' | 'mistral';

const URLS: Record<Service, string> = {
  claude: 'https://claude.ai/new',
  gpt: 'https://chatgpt.com/',
  deepseek: 'https://chat.deepseek.com/',
};

const EPS: Record<Provider, { url: string; model: string }> = {
  openai: { url: 'https://api.openai.com/v1/chat/completions', model: 'gpt-4o-mini' },
  deepseek: { url: 'https://api.deepseek.com/chat/completions', model: 'deepseek-chat' },
  mistral: { url: 'https://api.mistral.ai/v1/chat/completions', model: 'mistral-small-latest' },
};

const DEFAULT_PROMPT =
  'Razloži mi ta predpis v preprostem jeziku. Katere so najpomembnejše določbe in kaj pomenijo v praksi?';

const SYS =
  'Si pravni asistent. Odgovarjaš vedno v slovenščini, jasno in razumljivo, brez pravnega žargona. Pomagaš pri razlagi slovenskega pravnega besedila.';

function getLawText(): string {
  const el = document.querySelector('[data-pagefind-body]');
  return el instanceof HTMLElement ? el.innerText.slice(0, 6000) : '';
}

export function AiPanel({ lawName }: { lawName: string }) {
  const [question, setQuestion] = useState(DEFAULT_PROMPT);
  const [copyNote, setCopyNote] = useState('');
  const [provider, setProvider] = useState<Provider>('openai');
  const [apiKey, setApiKey] = useState('');
  const [response, setResponse] = useState('');
  const [busy, setBusy] = useState(false);
  const keyRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const k = localStorage.getItem('trubar_ai_key');
    const p = localStorage.getItem('trubar_ai_prov');
    if (k) setApiKey(k);
    if (p === 'openai' || p === 'deepseek' || p === 'mistral') setProvider(p);
  }, []);

  async function copyToService(service: Service) {
    const text = getLawText();
    const prompt =
      `Pravni predpis: ${lawName}\n\n` +
      text.slice(0, 4000) +
      (text.length > 4000 ? '\n[besedilo je skrajšano zaradi dolžine]\n' : '\n') +
      `\nVprašanje: ${question}`;
    try {
      await navigator.clipboard.writeText(prompt);
      setCopyNote(
        'Besedilo je bilo kopirano v odložišče. Ko se odpre pogovorno okno AI, prilepite ga (Ctrl+V oz. Cmd+V).',
      );
    } catch {
      setCopyNote('');
    }
    window.open(URLS[service], '_blank', 'noopener');
  }

  async function sendApi() {
    if (!apiKey) {
      setResponse('Prosim vnesite API ključ.');
      return;
    }
    localStorage.setItem('trubar_ai_key', apiKey);
    localStorage.setItem('trubar_ai_prov', provider);
    const ep = EPS[provider];
    const text = getLawText();
    const userMsg = `Predpis: ${lawName}\n\n${text}\n\nVprašanje: ${question}`;
    setBusy(true);
    setResponse('Čakam na odgovor ...');
    try {
      const r = await fetch(ep.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
        body: JSON.stringify({
          model: ep.model,
          messages: [
            { role: 'system', content: SYS },
            { role: 'user', content: userMsg },
          ],
          max_tokens: 1200,
        }),
      });
      const data = (await r.json()) as {
        choices?: Array<{ message?: { content?: string } }>;
        error?: { message?: string };
      };
      const msg =
        data.choices?.[0]?.message?.content ?? data.error?.message ?? JSON.stringify(data);
      setResponse(msg);
    } catch (e) {
      setResponse(`Napaka: ${(e as Error).message}`);
    } finally {
      setBusy(false);
    }
  }

  const btn =
    'rounded-md border border-border bg-card px-3 py-1.5 text-sm font-medium hover:bg-muted disabled:opacity-50';

  return (
    <details className="mt-10 rounded-md border border-border bg-card/50 p-4 open:bg-card">
      <summary className="cursor-pointer text-sm font-semibold">
        Vprašajte umetno inteligenco o tem predpisu
      </summary>

      <div className="mt-4 space-y-3">
        <textarea
          rows={3}
          spellCheck={false}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full rounded border border-border bg-background p-2 text-sm"
        />

        <div className="flex flex-wrap gap-2">
          <button type="button" className={btn} onClick={() => copyToService('claude')}>
            Odpri v Claudu (Anthropic)
          </button>
          <button type="button" className={btn} onClick={() => copyToService('gpt')}>
            Odpri v ChatGPT
          </button>
          <button type="button" className={btn} onClick={() => copyToService('deepseek')}>
            Odpri v DeepSeek
          </button>
        </div>

        {copyNote ? <p className="text-xs text-muted-foreground">{copyNote}</p> : null}

        <details className="mt-3 rounded border border-border p-3">
          <summary className="cursor-pointer text-sm">Imam lasten API ključ (napredno)</summary>

          <div className="mt-3 space-y-2">
            <p className="text-xs text-muted-foreground">
              API ključ dobite pri ponudniku (npr.{' '}
              <a
                href="https://platform.openai.com/api-keys"
                target="_blank"
                rel="noopener"
                className="underline"
              >
                OpenAI
              </a>
              ,{' '}
              <a
                href="https://platform.deepseek.com/"
                target="_blank"
                rel="noopener"
                className="underline"
              >
                DeepSeek
              </a>
              ). Ključ se hrani le v vašem brskalniku.
            </p>

            <div className="flex flex-wrap gap-2">
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value as Provider)}
                className="rounded border border-border bg-background px-2 py-1 text-sm"
              >
                <option value="openai">ChatGPT (OpenAI)</option>
                <option value="deepseek">DeepSeek</option>
                <option value="mistral">Mistral</option>
              </select>
              <input
                ref={keyRef}
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="API ključ (sk-...)"
                autoComplete="off"
                className="min-w-[200px] flex-1 rounded border border-border bg-background px-2 py-1 text-sm"
              />
              <button type="button" onClick={sendApi} disabled={busy} className={btn}>
                Pošlji
              </button>
            </div>

            {response ? (
              <pre className="mt-3 whitespace-pre-wrap rounded bg-muted p-3 text-xs">
                {response}
              </pre>
            ) : null}
          </div>
        </details>
      </div>
    </details>
  );
}
