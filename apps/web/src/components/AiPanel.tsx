'use client';

// Client island: AI assistant panel. Port of build_site.py:261-493, redesigned
// as a shadcn Dialog opened from a single button at the bottom of every law
// page.
//
// Two modes:
//  1. Copy-to-chat — copies a prompt to clipboard and opens claude.ai / chatgpt
//     / deepseek (works for any provider with a chat UI).
//  2. BYOK direct — sends the prompt directly to OpenAI / DeepSeek / Mistral
//     with the user's own API key (stored in localStorage). No Anthropic-direct
//     because their API doesn't allow browser-direct fetches without a proxy.

import { useEffect, useRef, useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

type Service = 'claude' | 'gpt' | 'deepseek';
type Provider = 'openai' | 'deepseek' | 'mistral';

const URLS: Record<Service, string> = {
  claude: 'https://claude.ai/new',
  gpt: 'https://chatgpt.com/',
  deepseek: 'https://chat.deepseek.com/',
};

const MODELS: Record<Provider, { label: string; models: { id: string; label: string }[]; url: string }> = {
  openai: {
    label: 'ChatGPT (OpenAI)',
    url: 'https://api.openai.com/v1/chat/completions',
    models: [
      { id: 'gpt-4o-mini', label: 'gpt-4o-mini (hitro, ceneje)' },
      { id: 'gpt-4o', label: 'gpt-4o (zmogljivejši)' },
      { id: 'gpt-4-turbo', label: 'gpt-4-turbo' },
    ],
  },
  deepseek: {
    label: 'DeepSeek',
    url: 'https://api.deepseek.com/chat/completions',
    models: [
      { id: 'deepseek-chat', label: 'deepseek-chat' },
      { id: 'deepseek-reasoner', label: 'deepseek-reasoner (sklepanje)' },
    ],
  },
  mistral: {
    label: 'Mistral',
    url: 'https://api.mistral.ai/v1/chat/completions',
    models: [
      { id: 'mistral-small-latest', label: 'mistral-small-latest' },
      { id: 'mistral-medium-latest', label: 'mistral-medium-latest' },
    ],
  },
};

const DEFAULT_PROMPT =
  'Razloži mi ta predpis v preprostem jeziku. Katere so najpomembnejše določbe in kaj pomenijo v praksi?';

const SYS =
  'Si pravni asistent. Odgovarjaš vedno v slovenščini, jasno in razumljivo, brez pravnega žargona. Pomagaš pri razlagi slovenskega pravnega besedila.';

const BODY_LIMIT = 6000;

function getLawText(): string {
  const el = document.querySelector('[data-pagefind-body]');
  return el instanceof HTMLElement ? el.innerText : '';
}

export function AiPanel({ lawName }: { lawName: string }) {
  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState(DEFAULT_PROMPT);
  const [copyNote, setCopyNote] = useState('');
  const [provider, setProvider] = useState<Provider>('openai');
  const [model, setModel] = useState<string>(MODELS.openai.models[0].id);
  const [apiKey, setApiKey] = useState('');
  const [response, setResponse] = useState<{ kind: 'idle' | 'loading' | 'ok' | 'err'; text: string }>(
    { kind: 'idle', text: '' },
  );
  const [bodyChars, setBodyChars] = useState(0);
  const dialogOpenedRef = useRef(false);

  // Defer reading localStorage + the law body until the Dialog opens — saves
  // work on pages where the user never asks anything.
  useEffect(() => {
    if (!open || dialogOpenedRef.current) return;
    dialogOpenedRef.current = true;
    const k = localStorage.getItem('trubar_ai_key');
    const p = localStorage.getItem('trubar_ai_prov');
    const m = localStorage.getItem('trubar_ai_model');
    if (k) setApiKey(k);
    if (p === 'openai' || p === 'deepseek' || p === 'mistral') {
      setProvider(p);
      if (m && MODELS[p].models.some((mm) => mm.id === m)) setModel(m);
    }
    setBodyChars(getLawText().length);
  }, [open]);

  // Reset the model when switching providers — the previous selection may not
  // exist for the new provider.
  useEffect(() => {
    setModel((current) => {
      const list = MODELS[provider].models;
      return list.some((m) => m.id === current) ? current : list[0].id;
    });
  }, [provider]);

  async function copyToService(service: Service) {
    const text = getLawText().slice(0, BODY_LIMIT);
    const truncated = text.length === BODY_LIMIT;
    const prompt =
      `Pravni predpis: ${lawName}\n\n${text}${truncated ? '\n[besedilo je skrajšano zaradi dolžine]\n' : '\n'}\nVprašanje: ${question}`;
    try {
      await navigator.clipboard.writeText(prompt);
      setCopyNote('Besedilo je kopirano v odložišče. Prilepite v pogovorno okno (Ctrl+V / Cmd+V).');
    } catch {
      setCopyNote('Odpiramo pogovor; besedila ni bilo mogoče samodejno kopirati.');
    }
    window.open(URLS[service], '_blank', 'noopener');
  }

  async function sendApi() {
    if (!apiKey) {
      setResponse({ kind: 'err', text: 'Prosim vnesite API ključ.' });
      return;
    }
    localStorage.setItem('trubar_ai_key', apiKey);
    localStorage.setItem('trubar_ai_prov', provider);
    localStorage.setItem('trubar_ai_model', model);
    const ep = MODELS[provider];
    const text = getLawText().slice(0, BODY_LIMIT);
    const userMsg = `Predpis: ${lawName}\n\n${text}\n\nVprašanje: ${question}`;
    setResponse({ kind: 'loading', text: 'Čakam na odgovor …' });
    try {
      const r = await fetch(ep.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
        body: JSON.stringify({
          model,
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
      if (data.error?.message) {
        setResponse({ kind: 'err', text: data.error.message });
        return;
      }
      const msg = data.choices?.[0]?.message?.content ?? JSON.stringify(data);
      setResponse({ kind: 'ok', text: msg });
    } catch (e) {
      setResponse({ kind: 'err', text: (e as Error).message });
    }
  }

  const truncated = bodyChars > BODY_LIMIT;
  const btnClass =
    'rounded-md border border-border bg-card px-3 py-1.5 text-sm font-medium hover:bg-muted disabled:opacity-50';

  return (
    <div className="mt-10 flex justify-center">
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger
          render={
            <button
              type="button"
              className="rounded-full border border-border bg-card px-5 py-2 text-sm font-medium shadow-sm hover:bg-muted"
            >
              ✨ Vprašaj AI o tem predpisu
            </button>
          }
        />
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Vprašaj AI o tem predpisu</DialogTitle>
            <DialogDescription>
              Pošljete vprašanje skupaj z besedilom predpisa izbranemu pomočniku. Kopiranje ne potrebuje
              ključa; neposreden klic potrebuje vaš API ključ.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4">
            <textarea
              rows={3}
              spellCheck={false}
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="w-full rounded border border-border bg-background p-2 text-sm"
            />

            <div className="space-y-2">
              <p className="text-xs font-medium text-muted-foreground">Odpri v pogovornem oknu</p>
              <div className="flex flex-wrap gap-2">
                <button type="button" className={btnClass} onClick={() => copyToService('claude')}>
                  Claude
                </button>
                <button type="button" className={btnClass} onClick={() => copyToService('gpt')}>
                  ChatGPT
                </button>
                <button type="button" className={btnClass} onClick={() => copyToService('deepseek')}>
                  DeepSeek
                </button>
              </div>
              {copyNote ? <p className="text-xs text-muted-foreground">{copyNote}</p> : null}
            </div>

            <details className="rounded border border-border p-3">
              <summary className="cursor-pointer text-sm font-medium">
                Neposreden klic z lastnim API ključem
              </summary>

              <div className="mt-3 space-y-3">
                <p className="text-xs text-muted-foreground">
                  Ključ se hrani le v vašem brskalniku. Poizvedba gre neposredno do ponudnika brez
                  posrednika. Anthropic (Claude) ni v tem seznamu, ker njihov API ne dovoli
                  brskalniških klicev.
                </p>

                <div className="grid gap-2 sm:grid-cols-2">
                  <label className="flex flex-col gap-1 text-xs">
                    <span className="text-muted-foreground">Ponudnik</span>
                    <select
                      value={provider}
                      onChange={(e) => setProvider(e.target.value as Provider)}
                      className="rounded border border-border bg-background px-2 py-1.5 text-sm"
                    >
                      {(['openai', 'deepseek', 'mistral'] as Provider[]).map((p) => (
                        <option key={p} value={p}>
                          {MODELS[p].label}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label className="flex flex-col gap-1 text-xs">
                    <span className="text-muted-foreground">Model</span>
                    <select
                      value={model}
                      onChange={(e) => setModel(e.target.value)}
                      className="rounded border border-border bg-background px-2 py-1.5 text-sm"
                    >
                      {MODELS[provider].models.map((m) => (
                        <option key={m.id} value={m.id}>
                          {m.label}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>

                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="API ključ (sk-…)"
                  autoComplete="off"
                  className="w-full rounded border border-border bg-background px-2 py-1.5 text-sm"
                />

                {truncated ? (
                  <p className="text-xs text-amber-700 dark:text-amber-300">
                    Pošljemo samo prvih ~{BODY_LIMIT.toLocaleString('sl-SI')} znakov besedila zakona
                    (od skupno {bodyChars.toLocaleString('sl-SI')}).
                  </p>
                ) : null}

                <button
                  type="button"
                  onClick={sendApi}
                  disabled={response.kind === 'loading'}
                  className={btnClass}
                >
                  Pošlji
                </button>

                {response.kind === 'loading' ? (
                  <p className="text-xs text-muted-foreground">{response.text}</p>
                ) : response.kind === 'err' ? (
                  <pre className="whitespace-pre-wrap rounded bg-rose-50 p-3 text-xs text-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
                    Napaka: {response.text}
                  </pre>
                ) : response.kind === 'ok' ? (
                  <pre className="whitespace-pre-wrap rounded bg-muted p-3 text-xs">
                    {response.text}
                  </pre>
                ) : null}
              </div>
            </details>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
