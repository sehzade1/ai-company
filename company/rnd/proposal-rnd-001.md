# Öneri rnd-001: Antigravity image-generator rolünün uzmanlaşması

Tarih: 2026-11-20 | Hazırlayan: R&D Direktörü | Kanıt gücü: ZAYIF (her hücrede 1 örnek)

## Hipotez
Tek bir genel `image-generator` rolü farklı iş türlerinde (logo, ürün fotoğrafı, editoryal illüstrasyon) tutarsız sonuç veriyor; tür-özel zanaat yönergeleri içeren kısa briefler kabul edilebilir çıktı oranını artırır.

## Kurulum
- Aynı kısa brief, iki varyant: GENERIC (`image-generator`) ve SPECIALISED (`rnd-image-logo`, `rnd-image-photo`, `rnd-image-illustration`). Üretim dosyalarına dokunulmadı.
- Briefler: A "Kuzey Kahve için logo"; B "açık gri stüdyo zeminde mat siyah seramik kupa"; C "küçük kafeli sonbahar sokak sahnesi, blog başlığı".
- Dosyalar nötr adlandırıldı (karıştırma): A1=generic, A2=spec; B1=spec, B2=generic; C1=generic, C2=spec. Konum: {{HOME}}\AppData\Local\Temp\claude\9519414f725d5b3e\010961af-914e-42f3-9dc3-0e3758650c0d\scratchpad\rnd-001\
- Puanlama: her görsel Read ile açıldı; tür uyumu, işçilik, yeniden işçilik gerektirmeden kullanılabilirlik (1-5). Puanlayan tek kişi (R&D), eşleşmeyi bilerek; ön yargı riski var.

## Sonuçlar
| Tür | GENERIC puan / token | SPECIALISED puan / token | Not |
|---|---|---|---|
| A Logo | 3 / 1181 | 4 / 1489 | Generic: pusula+çekirdek+buhar, fazla detay, 32px'te okunmaz. Spec: düz zemin, 2 renk, basit fincan+yıldız, okunaklı; yıldız/fincan kesişimi biraz garip |
| B Fotoğraf | 4 / 1234 | 4 / 1479 | İkisi de mat kupa, temiz stüdyo; spec biraz daha ortalı ve yumuşak gölge. Fark yok denecek kadar az |
| C İllüstrasyon | 2 / 1513 | 5 / 1706 | Generic fotogerçekçi çıktı (illüstrasyon değil) ve görsele uydurma "LA PETITE PAUSE" yazısı ekledi; spec tutarlı suluboya stil, sınırlı palet, başlık için boşluk, yazısız |
| Ortalama | 3.0 / 1309 | 4.3 / 1558 (+%19 token) | |

Toplam harcama ~17.7k token: geçerli 6 çağrı 8.6k + ilk denemede dosya yolu alıntı hatası yüzünden (6 görsel aynı dosyaya yazıldı) boşa giden 9.1k. Hata benim harness'imdeydi, rol hatası değil; deney bütçesi (20k) içinde kaldı.

## Sonuç
Uzmanlaşma logo ve illüstrasyonda anlamlı fark yarattı; fotoğrafta fark ölçülmedi. Spec brief çağrı başına ~%19 daha pahalı (daha uzun brief + daha uzun prompt/çıktı) ama yeniden çalışma ihtiyacını azaltıyor.

## Öneri
- BÖL: `image-logo` ve `image-illustration` (rnd- briefleri terfi ettirilebilir).
- BÖLME: fotoğraf için generic kalsın (veya `rnd-image-photo` yalnızca ek maliyet gerekçesi çıkarsa).
- Alternatif ucuz yol: roller yerine tek image-generator briefine tür bölümleri eklemek (yönetim yükü sıfır). Bu test edilmedi; pilotta karşılaştırılmalı.

## Kabul edilen teslimat başına tahmini maliyet (puan >=4 kabul)
- Önce (generic): 1/3 kabul; ~3.9k token / kabul edilen teslimat (kabaca 1309 x 3).
- Sonra (spec, 3 tür): 3/3 kabul; ~1.56k token / kabul edilen teslimat.
- Yalnızca logo+illüstrasyon bölünürse: logo ~1.49k, illüstrasyon ~1.71k, foto ~1.23k.
- Uyarı: n=1 ile bu oranlar istatistik değil, yön göstergesidir; kabul oranları gerçekte daha yumuşak olacaktır.

## Yönetim yükü
+2 rol briefi (roster, yönlendirme tablosu, HR notları), Direktörün tür-yönlendirme kararı. Düşük; brief başına ~1 küçük dosya.

## Takip pilotu için gerekenler
- Tür başına en az 3-5 farklı brief x 2 varyant (~30-40 çağrı, ~50k token; CEO onayı gerekir).
- Kör puanlama (varyant etiketi gizli) ve mümkünse ikinci puanlayıcı (Creative Director).
- Üçüncü varyant: tek brief içinde tür bölümleri.
- Logo için şeffaf PNG ve 32px okunabilirlik otomatik kontrolü; illüstrasyonda "yazı ekleme" ve foto/illüstrasyon karışması sayacı.
- Harness düzeltmesi: dosya yolu alıntılaması (görev adı boşluksuz, prompt'ta $ değişken kullanılmaz).
