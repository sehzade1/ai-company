# Direktörler toplantısı — CEO kararı (2026-11-20)

Katılımcılar: Mühendislik, Yaratıcı İşler, Operasyon direktörleri (Opus). Öneriler: engineering.md, creative.md, operations.md.
Karar kuralı: en az 2 direktörün aynı rolü aynı modele verdiği yerde çoğunluk; çatışmada kanıtlanmış yetenek ve çapraz denetim kuralı.

## Kanıtlanmış gerçekler (yoklamalardan)
- Codex sandbox'ı salt okunur: dosya yazamaz, test/build çalıştıramaz. Yazar rollerinde DIFF üretir; uygulamayı ve testi Claude yapar. (Yazma izni ancak kullanıcı onayıyla.)
- Antigravity dosya yazabildiğini, web araştırması yapıp kaynak gösterebildiğini, görsel/PDF okuyabildiğini ve bir image-generator alt ajanı olduğunu söylüyor. Görsel üretimi KANITLANMADI.
- Blender 5.1 yerelde kurulu (C:\Program Files\Blender Foundation\Blender 5.1\blender.exe). OpenSCAD yok. Node var.
- Hiçbir modelde doğrulanmış yerleşik görsel üretimi yok. Claude koddan görsel üretebilir (SVG/PIL/three.js/Blender).

## Kadro (model başına 5 rol)

| Model | Rol | Direktör | Güven | İnceleyen (çapraz) | Yedek |
|---|---|---|---|---|---|
| Codex | backend-developer | Mühendislik | Yüksek | Claude security-auditor + test-writer | Claude Sonnet |
| Codex | refactoring-specialist | Mühendislik | Yüksek | Claude test-writer | Claude Sonnet |
| Codex | bug-finder (yalnız başka modellerin kodunda) | Mühendislik | Yüksek | Mühendislik Direktörü (yeniden üretir) | Claude Sonnet |
| Codex | performance-optimizer | Mühendislik | Orta | Claude test-writer (benchmark) | Claude Sonnet |
| Codex | code-reviewer (Claude/Antigravity kodu) | Mühendislik | Orta-Yüksek | Mühendislik Direktörü | Claude Sonnet (yazar Claude değilse) |
| Claude | test-writer (testleri çalıştırabilen tek aktif model) | Mühendislik | Yüksek | Codex code-reviewer | Codex (diff) |
| Claude | security-auditor | Mühendislik | Yüksek | Mühendislik Direktörü | Codex code-reviewer |
| Claude | devops-ci | Mühendislik | Orta | Codex bug-finder | Codex (diff) |
| Claude | frontend-developer | Yaratıcı | Yüksek | Codex code-reviewer + Antigravity accessibility | Antigravity |
| Claude | ui-ux-designer | Yaratıcı | Yüksek | Antigravity accessibility + Yaratıcı Direktör | Antigravity |
| Antigravity | researcher | Operasyon | Yüksek | Operasyon Direktörü (kaynak kontrolü) | Claude Sonnet |
| Antigravity | data-analyst | Operasyon | Orta | Codex code-reviewer (hesap kodu) | Claude Sonnet |
| Antigravity | image-generator | Yaratıcı | Orta-Yüksek — pilot GEÇTİ (şeffaf arka plan yok) | Yaratıcı Direktör (dosyayı açıp inceler) | Claude (SVG/PIL ile kod tabanlı, kısıtlı) |
| Antigravity | 3d-modeler (Blender Python, headless) | Yaratıcı | Orta — TEST EDİLMELİ | Codex bug-finder (script) + Yaratıcı Direktör (render) | Claude Sonnet (Blender script) |
| Antigravity | accessibility-reviewer | Yaratıcı | Orta | Yaratıcı Direktör | Claude Sonnet (yazar Claude değilse) |
| Kimi | translator | Operasyon | Düşük — giriş bekliyor | Operasyon Direktörü (örnekleme) | Antigravity |
| Kimi | technical-writer | Yaratıcı | Düşük — giriş bekliyor | Claude (teknik doğruluk) | Antigravity |
| Kimi | copywriter | Yaratıcı | Düşük — giriş bekliyor | Yaratıcı Direktör | Claude Haiku |
| Kimi | prompt-engineer (görsel/ajan brief'leri) | Yaratıcı | Düşük — giriş bekliyor | Yaratıcı Direktör | Claude Sonnet |
| Kimi | bulk-drafter (toplu taslak/içerik) | Operasyon | Düşük — giriş bekliyor | Operasyon Direktörü (örnekleme) | Claude Haiku |

## Çözülen anlaşmazlıklar
1. UI/UX: Mühendislik Antigravity'yi istedi, iki direktör Claude dedi. Karar: Claude. Tarafsız denetim Codex code-reviewer + Antigravity accessibility ile sağlanıyor.
2. Bug-finder: Operasyon Kimi'yi önerdi (henüz çalışmıyor). Karar: Codex (iki direktör), yalnızca başka modellerin kodunda.
3. Test-writer: Codex test çalıştıramıyor. Karar: Claude.
4. Görsel/3D: hepsi Antigravity'de, ama ilk görevden önce pilot test zorunlu. Kanıt yoksa rol Claude'un kod tabanlı yedeğine düşer.
5. Kimi: 5 rolün hepsi geçici vekillerle yürür. Girişten sonra 1 çeviri + 1 metin pilotu geçmeden devretme yok.
6. Kod incelemesi Claude'da yığılmasın diye Codex'e code-reviewer rolü verildi (Claude'un ve Antigravity'nin kodu için).

## Finans kararları
- Fallback rol bazında (yukarıdaki tablo). Bir model tükenince aynı anda en fazla 2 rol devredilir.
- Kimi giriş yapana kadar hiçbir yedek listesinde yer almaz.
- Claude'a yumuşak bütçe ve `company.ps1 log` ile elle kayıt.
- Gerçek bütçe rakamları kullanıcıdan bekleniyor. Codex sayıları gerçek, diğerleri tahmin; karşılaştırırken dikkat.

## Ek karar (CEO, kullanıcı talebiyle): TestSprite
TestSprite dış QA tedarikçisi olarak Mühendislik Direktörü'ne bağlandı; Claude test-writer kullanır, Codex code-reviewer test sonuçlarını inceleyebilir. Kredi takibi Finans'ta. Bulut/tünel kullanımı proje bazında kullanıcı onayına bağlı. Yeni ajan slotu açılmadı (model başına 5 rol korunuyor).

## Ek karar (CEO, kullanıcı talebiyle, 2026-11-20): yapı güncellemesi
- Direktörler Opus'tan Sonnet'e geçti (fiyat/performans). Opus yalnızca CEO.
- Ar-Ge Departmanı kuruldu (`director-rnd`, Sonnet). İK Müdürü (`manager-hr`, Haiku) ve Finans Müdürü (`manager-finance`, Sonnet) Operasyon Direktörü altında.
- "Model başına 5 ajan" kuralı kaldırıldı: kadro kanıta göre değişir. Rol ekleme/bölme/emekliye ayırma: Ar-Ge pilotu → Ar-Ge + İK + Finans fiyat/performans toplantısı → CEO kararı.
- Ar-Ge'nin ilk gündemi: rnd/experiments.md içindeki backlog (ilk aday: görsel üreticiyi türlere göre uzmanlaştırmak).

## Ek karar: rnd-001 (fiyat/performans toplantısı, 2026-11-20) — ayrıntı: meeting\rnd-001-meeting.md
| Model | Rol | Direktör | Güven | İnceleyen | Yedek |
|---|---|---|---|---|---|
| Antigravity | image-illustration (editoryal/blog/kapak illüstrasyonu) | Yaratıcı | Orta (n=1, net kategori farkı) | Yaratıcı Direktör | Claude (kod tabanlı, kısıtlı) |
- image-generator artık: ürün/nesne fotoğrafı + logo/ikon (rnd-002 sonuçlanana kadar).
- image-logo: deneysel (roles\antigravity\rnd-image-logo.md), üretimde kullanılmaz.
- Yönlendirme: belirsiz görsel işlerinde Yaratıcı Direktör hangi role gideceğine karar verir.
- rnd-002 takip pilotu onaylı (36k tavan), kullanıcının başlat onayını bekliyor.

## Ek karar: rnd-002 logo kolu (CEO, 2026-11-20)
Kör puanlama, iki puanlayıcı (Claude Yaratıcı Direktör + Codex), 4 logo brief'i:
| Varyant | Ort. puan | Kabul |
|---|---|---|
| image-generator (genel) | 2.67 | 0/3 |
| rnd-image-logo (uzman) | 4.0 | 4/4 |
| rnd-image-sections (tek brief, bölümlü) | 4.0 | 3/4 |
Karar: **image-logo üretime alındı** (Antigravity, Yaratıcı, inceleyen: Yaratıcı Direktör, yedek: Claude SVG). image-generator artık ürün/nesne fotoğrafı + uzman rolü olmayan türler. rnd-image-sections ile ayrı roller arasındaki nihai seçim illüstrasyon kolundan sonra (kota nedeniyle illüstrasyon kolu yeniden çalıştırılacak).
Not: token tahminleri bu turda güvenilmez (zaman aşımına uğrayan çağrılar kısmi çıktıyla kaydedildi); karar kaliteye dayanıyor.

## Ek karar: Kimi çıkarıldı (kullanıcı onayıyla, 2026-11-20)
Sebep: abonelik Kimi Code erişimi içermiyor (HTTP 403). Rol dosyaları roles\_retired\kimi\ altında saklanıyor. Vekiller kalıcı sahip oldu:
| Rol | Yeni sahip | Dosya | İnceleyen | Yedek |
|---|---|---|---|---|
| translator | Antigravity | roles\antigravity\translator.md | Operasyon Direktörü | Claude Haiku |
| technical-writer | Antigravity | roles\antigravity\technical-writer.md | Claude (teknik doğruluk) | Claude Sonnet |
| copywriter | Claude Haiku | worker-claude-copywriter | Yaratıcı Direktör | Claude Sonnet |
| prompt-engineer | Claude Sonnet | worker-claude-prompt-engineer | Yaratıcı Direktör | Antigravity |
| bulk-drafter | Claude Haiku | worker-claude-bulk-drafter | Operasyon Direktörü | Antigravity |
Yukarıdaki tablolardaki Kimi satırları geçersizdir.

## Ek karar: yerel model işe alındı (CEO, rnd-003, 2026-11-20)
Ajan `local` = Ollama + Gemma 3 12B (Q4_K_M, RTX 3060'ta %100 GPU). Ücretsiz, kota yok, veri bilgisayardan çıkmaz, gerçek token sayısı.
rnd-003 (Codex kör puanlama, n=1): çeviri local 4.3 vs Haiku 3.7; toplu açıklama local 2.0 (İngilizce yazdı) vs Haiku 5.0; özet local 3.3 (ayrıntı atladı) vs Haiku 5.0.
| Model | Rol | Direktör | İnceleyen | Yedek |
|---|---|---|---|---|
| local | translator-draft (yüksek hacimli ilk çeviri; Antigravity translator son okumayı yapabilir) | Operasyon | Operasyon Direktörü | Antigravity translator |
| local | private-worker (kişisel/gizli veri içeren işler: maskeleme, çıkarma, sınıflandırma, kısa özet) | atayan direktör | atayan direktör | yok — gizli veri buluta gönderilmez; kullanıcıya sorulur |
bulk-drafter ve özetler Claude Haiku'da kalır.

## Ek karar: yerel görsel üretimi işe alındı (CEO, 2026-11-21)
Ajan `local-image` = ComfyUI 0.46.0 + FLUX.1-schnell fp8 (Apache-2.0), D:\AI\ComfyUI_windows_portable, RTX 3060. Ücretsiz, kota yok, veri bilgisayardan çıkmaz, ~20-25 sn/görsel.
Pilot (CEO incelemesi, n=1): logo 5/5 (metin hatasız, 2 renk, sade); illüstrasyon 3.5/5 (stil iyi ama "yazı yok" talimatına rağmen uydurma tabela yazıları — schnell negatif talimatı uygulamıyor).
| Rol | Birincil | Yedek | Not |
|---|---|---|---|
| Logo / ikon / amblem | Antigravity image-logo VEYA local-image (Yaratıcı Direktör seçer) | diğeri | Çok varyant gerekiyorsa local-image (ücretsiz) |
| Editoryal illüstrasyon | Antigravity image-generator (rnd-002b) | local-image (yazısız gerekiyorsa çıktıyı kontrol et) | |
| Ürün fotoğrafı / diğer | Antigravity image-generator | local-image | |
| Antigravity görsel kotası dolduğunda | local-image | Claude kod tabanlı | Artık görsel işi durmaz |
| Gizli/özel görseller | local-image | — | Buluta gönderilmez |
Açık konu (Ar-Ge backlog): local-image vs Antigravity kör karşılaştırması; şeffaf PNG için arka plan kaldırma.

## Raporlama zinciri
Çalışan → ilgili Direktör (doğrular, puanlar, özetler) → CEO → kullanıcı. Çalışan CEO'ya doğrudan rapor vermez.

## Addendum 2026-11-21: model per role (rnd-004)
Role files now carry `model:` / `effort:` in frontmatter; company.ps1 passes them (`-m`/`-c model_reasoning_effort` for Codex, `--model`/`--effort` for Antigravity). `-Model`/`-Effort` on the command line override.
- Codex, all roles: gpt-6-luna, effort medium. Fallback gpt-5.6-terra.
- Antigravity text roles: gemini-4-hydrogen-high. Fallback gemini-3.8-flash-medium, then gemini-4-neon-high (rnd-009). Image roles unchanged.
Details: rnd\rnd-004\results.md
## Addendum 2026-11-21: Codex effort (rnd-005)
bug-finder and code-reviewer: gpt-6-luna effort high. Other Codex roles: medium. Details: rnd\rnd-005\results.md

## Addendum 2026-11-21: illustration arm (rnd-002b)
Generic image-generator 4.67, specialist 4.5-4.67, sections 4.5-4.67 (all 3/3 accepted, blind, 2 scorers); local FLUX 2.67-3.33 (0/3, invented text). image-illustration and rnd-image-sections retired; illustrations go to image-generator. image-logo stays. Antigravity quota: ~9 images per ~4.5 h. Details: rnd\rnd-002b\results.md

## Addendum 2026-11-22: 3D modeler (rnd-007)
Antigravity 3d-modeler passed (cup 4.5, chest 4.5, both ran first try) and is in production. It replies with a Blender script; the CEO runs Blender headless. Codex: fallback modeller and script reviewer. Details: rnd\rnd-007\results.md

## Addendum 2026-11-22: review model (rnd-008)
Copy reviews and translation spot-checks: Claude Haiku (same accuracy as Sonnet, cleaner). Sonnet: directors and spec-less judgement. Short checks: prefer Codex or local model over a Claude subagent (~50k overhead). Details: rnd\rnd-008\results.md

## Addendum 2026-11-22: Gemini fallback order (rnd-009)
hydrogen-high, neon-high and flash-medium tied on 4 more objective tasks; hydrogen fastest and stays default. Fallback order: gemini-3.8-flash-medium, then gemini-4-neon-high. Details: rnd\rnd-009\results.md
