# Fiyat/performans toplantısı — rnd-001 (2026-11-20)

Katılımcılar: Ar-Ge Direktörü (öneri), İK Müdürü, Finans Müdürü. Karar: CEO.
Girdi: rnd\proposal-rnd-001.md, rnd\experiments.md, ledger.csv. CEO illüstrasyon çiftini (C1/C2) bizzat inceledi.

## Oylar
| Konu | Ar-Ge | İK | Finans | CEO kararı |
|---|---|---|---|---|
| image-illustration ayrı rol | Onay | Pilot-daha | Onay | ONAY |
| image-logo ayrı rol | Onay | Pilot-daha | Pilot-daha | PİLOT-DAHA (rnd-image-logo deneysel kalır) |
| Foto için uzman | Bölme yok | — | Ret | RED (image-generator foto için kalır; rnd-image-photo arşivlendi) |
| Takip pilotu rnd-002 | ~50k | Koşullu onay | ~36k tavan | ONAY, 36k tavan, kullanıcının başlat onayıyla |

## Gerekçe
- İllüstrasyonda genel rol bir kategori hatası yaptı (illüstrasyon yerine fotoğraf + uydurma tabela). Bu zevk farkı değil, CEO doğruladı. Kabul edilen teslim başına maliyet ~3.9k → ~1.56k (Finans, ledger ile doğrulandı). Yapısal maliyet: +1 rol.
- Logo farkı (3'e 4) gürültü sınırında; tek örnek yetersiz.
- Ar-Ge'nin betik hatasıyla harcanan ~9.1k token deney maliyetidir, role yazılmaz.

## Uygulanan değişiklikler
- roles\antigravity\image-illustration.md üretime alındı (rnd taslağı _retired\ altına arşivlendi).
- roles\_retired\antigravity\rnd-image-photo.md arşivlendi.
- Yönlendirme kuralı (İK önerisi): logo/ikon/rozet → image-generator (rnd-002 sonuçlanana kadar); editoryal/blog sahnesi, kitap/kapak illüstrasyonu → image-illustration; ürün/nesne fotoğrafı → image-generator. Belirsizse Yaratıcı Direktör karar verir.
- Yedek: image-illustration → Claude (kod tabanlı, "kısıtlı" etiketiyle).

## rnd-002 şartları (takip pilotu)
Sadece logo + illüstrasyon; tür başına 4 brief × 3 varyant (genel / uzman / tek brief içinde tür bölümleri) = 24 çağrı, ~36k token tavanı. Kör puanlama: Yaratıcı Direktör + ikinci puanlayıcı. Üçüncü varyant kazanırsa rol bölmeye gerek kalmaz. Başlamadan önce `company.ps1 status` kontrolü.

## Finans notu (CEO)
Yönetim katmanı pahalı: bu toplantı ve pilotta Claude ajanları ~241k token harcadı (Ar-Ge ~100k, İK ~74k, Finans ~68k), işçi görsel çağrıları ise ~17.7k. Bundan sonra küçük kararlar tek müdürle ya da doğrudan CEO tarafından verilmeli; toplantılar yalnızca yapısal kararlar için.
