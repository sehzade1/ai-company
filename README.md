# AI Company for Claude Code

Claude Code'u bir **yapay zeka şirketi** gibi çalıştıran kurulum. Ana oturum CEO'dur (Claude Opus); işi
modellerin güçlü olduğu alanlara göre Claude, OpenAI Codex ve Google Antigravity/Gemini ajanlarına
dağıtır, çıktıları başka bir modele çapraz inceletir ve Finans departmanı her çağrının token
harcamasını kaydeder. Rol ve model kararları, cevap anahtarlı kör testlerle (Ar-Ge) verilir.

*A Claude Code setup that runs as an AI company: the main session is the CEO, work is routed to
Claude, Codex and Gemini agents by measured strength, cross-reviewed, and every call is logged by a
Finance ledger. Role and model choices come from blind, answer-keyed R&D tests (see `company/rnd/`).*

## Yapı

```
CEO (Claude Opus, ana oturum)
├── Direktörler (Claude Sonnet): Mühendislik, Yaratıcı, Operasyon, Ar-Ge
│   └── Operasyon altında: İK (Haiku), Finans (Sonnet)
└── İşçiler
    ├── Claude: test, güvenlik, frontend, UI/UX, metin, toplu taslak, prompt
    ├── Codex (gpt-6-luna): backend, hata avı, refaktör, performans, kod inceleme (salt okunur)
    ├── Antigravity/Gemini (gemini-4-hydrogen-high): araştırma, veri, çeviri, teknik yazı,
    │   erişilebilirlik, görsel (logo uzmanı + genel), 3D (Blender script)
    └── Yerel: Ollama gemma3:12b (gizli veri, çeviri taslağı), ComfyUI FLUX (yedek görsel)
```

Ayrıntı: [`company/ORG.md`](company/ORG.md), kararlar: [`company/meeting/decision.md`](company/meeting/decision.md),
Ar-Ge sonuçları: [`company/rnd/`](company/rnd/).

## Öne çıkan Ar-Ge bulguları

| Test | Sonuç |
|---|---|
| rnd-004/005 | Codex'te gpt-6-luna en iyi ve en ucuz; hata avı ve kod incelemede `high` effort 7/7 ve 9/9 buldu (low/medium 6/7, 8/9) |
| rnd-004/009 | Gemini modelleri 6 nesnel görevde eşit; hydrogen-high en hızlı |
| rnd-002 | Logo için uzman brief kazandı; illüstrasyonda uzman brief fark yaratmadı |
| rnd-007 | 3D: Antigravity Blender script'leri 2/2 ilk denemede çalıştı (Codex 1/2) |
| rnd-008 | Kontrol listesi tipi incelemede Haiku = Sonnet; Claude alt ajanı çağrı başına ~50k token yük getirir |

## Kurulum (Windows)

1. [Claude Code](https://claude.com/claude-code) kurulu olsun.
2. Repoyu indir ve çalıştır:
   ```powershell
   git clone <bu repo> ; cd ai-company
   powershell -ExecutionPolicy Bypass -File .\install.ps1
   ```
   Var olan dosyalar `~\.claude\backup-<tarih>` altına yedeklenir.
3. İstediğin ajanları kur (hepsi isteğe bağlı; olmayan ajanın işi yedeğine gider):
   - OpenAI Codex CLI, Google Antigravity CLI (`agy`)
   - Ollama + `gemma3:12b` (yerel metin), ComfyUI + FLUX.1-schnell (yerel görsel)
   - Blender (3D), Python 3 + Pillow, numpy, scipy (şeffaf PNG aracı)
4. `~\.claude\company\budgets.json` içindeki günlük bütçeleri kendi planlarına göre ayarla.
5. Claude Code'u yeniden başlat.

## Kullanım

- Herhangi bir projede önemsiz olmayan her iş şirket akışıyla yürür (global `CLAUDE.md`).
- Finans raporu: `powershell -File ~\.claude\company\company.ps1 report`
- Yeni ve temiz proje: `powershell -File ~\.claude\company\tools\new-project.ps1 -Name proje-adi [-Type game]`
- Oyun projeleri için [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
  alt şirket olarak çalışır; yönlendirme kuralı `company/studio-template/ai-company-routing.md`.

## Güvenlik ilkeleri

İşçiler salt okunur ya da kısıtlı çalışır; izin atlatma bayrakları kullanıcı onayı olmadan kullanılmaz.
İşçi çıktısı veridir, talimat değildir. Gizli veriler dış servislere değil yerel modele gider.
Repo kişisel veri, API anahtarı veya kullanım kaydı (`ledger.csv`) içermez.
