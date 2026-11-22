# Operasyon Direktörlüğü önerisi: worker kadrosu (20 rol)

Bakış açısı: maliyet, iş hacmi, araştırma kalitesi, erişilebilirlik ve bütçe dengesi.
Kanıt: roster.md, ORG.md, budgets.json ve Antigravity'ye yapılan tek yetenek sorusu (2026-11-20). Antigravity'nin cevabı modelin kendi beyanıdır, doğrulanmış bir test sonucu değildir.

## Antigravity probu (kendi beyanı)
- Canlı web araması `search_web` ile yapılıyor ve URL kaynakları veriyor (beyan).
- Pratik bağlam penceresi: kendisi de "bilinmiyor" dedi. Uzun bağlam iddiası **test edilmeli**.
- Resim ve PDF okuma `read_file` ile yapılıyor (beyan).
- Resim üretimi `image-generator` alt ajanıyla yapılıyor (beyan). **Test edilmeli.**
- CLI modunda dosya yazıp düzenleyebiliyor (beyan). Bu yüzden worker'ın salt-okunur kalması kuralı açıkça uygulanmalı.
- Zayıf yanlar: CAPTCHA, sandbox sınırları, doğrulanmamış tahmin.
- Maliyet: 302 token (tahmini, chars/4), günlük bütçenin %0.1'i.

## Rol ataması

| Model | Rol | Gerekçe | Güven | Yedek |
|---|---|---|---|---|
| Codex | Backend geliştirici | Kodlama ajanı, sandbox'ta çalışıyor ve gerçek token sayısı veriyor. En büyük hacmi ölçülebilir modele vermek Finans için en sağlıklısı. | high | Claude Sonnet |
| Codex | Test yazarı | Testleri yazan aynı sandbox'ta çalıştırabiliyor; iş hacmi yüksek ve tekrarlayan bir iş. | high | Claude Sonnet |
| Codex | Refactoring uzmanı | Çok dosyalı mekanik değişiklik kodlama ajanına uygun. Gözden geçirmeyi Claude yapar (yazar kendi işini incelemez). | medium | Claude Sonnet |
| Codex | DevOps/CI | Script ve pipeline dosyası üretimi. Sandbox gerçek deploy'u engeller, bu da operasyonel olarak güvenli. | medium | Claude Sonnet |
| Codex | Performans optimizasyoncusu | Ölçüp karşılaştırmak için kod çalıştırmak gerekiyor. Sandbox'ta benchmark kısıtları olabilir, **test edilmeli**. | medium | Antigravity |
| Claude (Sonnet/Haiku) | Frontend geliştirici | Tüm araçlar, dosya düzenleme ve tarayıcı erişimi var; görsel doğrulamayı da yapabilir. | high | Codex |
| Claude (Sonnet/Haiku) | UI/UX tasarımcı | ORG'da zaten Design & Docs Claude'da; design skill'leri mevcut. | high | Antigravity |
| Claude (Sonnet) | Kod inceleyici | Kodun çoğunu Codex yazdığı için inceleme farklı bir modelde kalıyor (cross-review kuralı). | high | Antigravity |
| Claude (Sonnet) | Güvenlik denetçisi | Yüksek riskli ve düşük hacimli bir iş. En güvenilir araç erişimi burada, security-review skill'i de var. | medium | Codex (salt-okunur) |
| Claude (Sonnet) | Ürün yöneticisi | Karar ağırlıklı ve CEO'ya yakın bir iş. Hacmi düşük olduğu için ölçülmeyen kullanım riski küçük. | medium | Antigravity |
| Antigravity | Araştırmacı | Web araması ve kaynak gösterimi var (beyan); ORG'da Research başkanı. Kaynaklar yine de Operasyon tarafından kontrol edilecek. | high | Claude Sonnet (WebSearch) |
| Antigravity | Veri analisti | Uzun doküman ve PDF/resim okuma (beyan), araştırmaya yakın bir iş. Bağlam sınırı bilinmiyor, **test edilmeli**. | medium | Claude Sonnet (data skill'leri) |
| Antigravity | Görsel üretici | 4 model içinde resim üretebildiğini söyleyen tek model (`image-generator`, beyan). | low (**test edilmeli**) | Yok: dışarıdan bir araç gerekir ya da SVG/kod ile görsel üretimi Claude yapar |
| Antigravity | 3D modelci (Blender Python / three.js / OpenSCAD) | Multimodal olduğu için render çıktısını kendisi kontrol edebilir. Codex'in yükünü dengeler. | low (**test edilmeli**) | Codex |
| Antigravity | Erişilebilirlik denetçisi | Ekran görüntüsünü okuyarak kontrast ve düzen incelemesi yapabilir; frontend'i yazan Claude'dan farklı bir model. | medium | Claude Sonnet (design:accessibility-review) |
| Kimi (BEKLEMEDE) | Çevirmen | ORG'a göre Operations başkanı, toplu iş ve çeviri ucuz hacim işi. Login'e kadar kullanılamaz. | low (**test edilmeli**) | Antigravity |
| Kimi (BEKLEMEDE) | Metin yazarı (copywriter) | Taslak ve varyasyon üretimi yüksek hacimli ve ucuz bir iş. Son düzeltmeyi Claude yapar. | low (**test edilmeli**) | Claude Haiku |
| Kimi (BEKLEMEDE) | Teknik yazar | README ve doküman taslakları toplu iş. Claude'un ölçülmeyen kullanımını azaltır. | low (**test edilmeli**) | Claude Haiku |
| Kimi (BEKLEMEDE) | Hata avcısı (bug finder) | Geniş kod taraması hacim işi; bulguları Codex/Claude doğrular. Kod okuma kalitesi bilinmiyor. | low (**test edilmeli**) | Codex (salt-okunur) |
| Kimi (BEKLEMEDE) | Prompt mühendisi | Diğer ajanlar için şablon ve brief taslakları üretir, düşük riskli. | low (**test edilmeli**) | Claude Sonnet |

Dağılım: her modelde 5 rol, toplam 20. Kodlama hacmi Codex'te, karar ve inceleme Claude'da, araştırma ve multimodal işler Antigravity'de, metin hacmi Kimi'de.

## (a) Kimi login olana kadar geçici yedekler

| Kimi rolü | Geçici yedek | Not |
|---|---|---|
| Çevirmen | Antigravity | Bütçe kullanımı %0.1, bol yer var. |
| Metin yazarı | Claude Haiku | Ucuz ve hızlı. Kullanım `company.ps1 log` ile elle kaydedilmeli. |
| Teknik yazar | Antigravity | Claude'a yük bindirmemek için. Son okumayı Claude Sonnet yapar. |
| Hata avcısı | Codex (salt-okunur) | Token sayısı gerçek ölçülüyor. Bulguları Claude doğrular. |
| Prompt mühendisi | Claude Sonnet | Düşük hacim. |

Login sonrası adım: Kimi'ye küçük bir pilot iş verilir (1 çeviri + 1 kod taraması). İK sonucu roster'a yazar, rol ancak bundan sonra devredilir.

## (b) Bütçe bitince yedek kuralları
- Tabloda her rolün "Yedek" sütunu var. Kural: yedek, işi inceleyen modelle aynı olmamalı. Olursa inceleme üçüncü modele geçer.
- EXHAUSTED olan model aynı anda en fazla 2 rolünü yedeğe devretmeli, yoksa yedek model WARNING seviyesine itilir. Kalan işler ertelenir ve CEO'ya bildirilir.
- Codex bütçesi biterse: kodlama işleri Claude Sonnet'e geçer, performans işi Antigravity'ye geçer.
- Antigravity bütçesi biterse: araştırma Claude'un WebSearch'üne geçer. Görsel üretim için yedek yok, iş ertelenir.

## (c) budgets.json hakkında notlar
1. **Tutarlılık sorunu:** 500000 değeri Codex'te gerçek token, Antigravity ve Kimi'de chars/4 tahmini. Aynı sayı bu üç model için aynı anlama gelmiyor. Gerçek plan limitleri bilinmiyor, ben de sayı uydurmuyorum. Kullanıcı provider limitlerine göre düzeltmeli.
2. **Claude ölçülmüyor (0):** 5 rol taşıyan bir modelin görünmemesi Finans için kör nokta. Öneri: `claude-sonnet` için tahmini bir "yumuşak" bütçe konsun ve her alt ajan çağrısı `company.ps1 log` ile kaydedilsin.
3. **Kimi:** login yokken 500000 anlamsız, durumu "pending" olarak ayrıca işaretlenmeli. Antigravity'nin yedek listesinde 2. sırada Kimi var; şu an çalışmayan bir yedek.
4. **Döngü riski:** Claude Sonnet'in yedeği Codex, Codex'in yedeği Claude Sonnet. İkisi birden tükenirse iş Antigravity'ye yığılır. Ayrıca ajan bazlı yedek listesi kod dışı işlerde (metin, tasarım) Codex'i önerebiliyor. Yedek seçimi rol bazlı yapılmalı (yukarıdaki tablo).
5. Uyarı eşikleri (70/90) makul.
6. Hacim tahmini (test edilmeli): en çok yük Codex'te olacak (5 kodlama rolü). Codex'in limiti diğerlerinden önce gözden geçirilmeli.
