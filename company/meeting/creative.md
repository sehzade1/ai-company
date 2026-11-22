# Kreatif Direktör Önerisi: 20 Çalışan Ajan Dağılımı

Tarih: 2026-11-20. Bakış açısı: tasarım, görsel, görüntü üretimi, 3D, metin, dokümantasyon.
İlke: Görsel ve 3D işler, dosya yazıp çalıştırabilen ve sonucu gözle kontrol edebilen ajana verilir. Bir ajanın kendi beyanı kanıt sayılmaz; doğrulanmamış yetenekler "test edilmeli" olarak işaretlendi.

| Model | Rol | Gerekçe | Güven |
|---|---|---|---|
| Antigravity | Görüntü üretici (image generator) | `image-generator` alt ajanının bu oturumda kayıtlı olduğunu söylüyor; dört model içinde yerleşik görüntü üretimi olan tek aday bu. Gerçek PNG üretimi test edilmeli | orta (test edilmeli) |
| Antigravity | 3D modelleyici (Blender Python) | Blender 5.1.1'i bulup çalıştırabildiğini söyledi; blender.exe'nin varlığını yerelde doğruladım. Headless render ve .glb/.stl dışa aktarımı test edilmeli | orta-yüksek |
| Antigravity | Araştırmacı (görsel referans / moodboard) | Research bölümünün başı; web ve çok modlu yetenekleri referans toplamaya uygun | yüksek |
| Antigravity | Görsel QA / sanat eleştirmeni | Görüntüleri `read_file` ile okuyup değerlendirebildiğini söylüyor; Claude'un ürettiği görselleri çapraz incelemek için iyi | orta |
| Antigravity | Erişilebilirlik denetçisi | Ekran görüntüsü ve kod üzerinden kontrast/etiket incelemesi yapabilir; Claude'un UI işlerine bağımsız gözle bakar | orta |
| Claude (Sonnet) | UI/UX tasarımcı | Tam araç erişimi, dosya düzenleme, artifact/HTML önizleme; tasarım ve dokümantasyon sorumluluğu zaten Claude'da | yüksek |
| Claude (Sonnet) | Frontend geliştirici (three.js / SVG / CSS) | Görsel bileşenleri yazar ve tarayıcıda çalıştırıp kontrol eder; kod tabanlı görseller (SVG, three.js sahnesi) de bu rolde. Node kurulu | yüksek |
| Claude (Sonnet) | Teknik yazar | README, kullanım kılavuzu ve spec yazımında güçlü; dosya yazma yetkisi var | yüksek |
| Claude (Sonnet) | Metin yazarı / UX copy | Ton tutarlılığı, mikro metinler, pazarlama metni | yüksek |
| Claude (Haiku) | Prompt mühendisi (görsel brief yazarı) | Antigravity'nin image-generator'ına giden brief'leri standart şablona sokar; ucuz ve hızlı | orta |
| Codex | Backend geliştirici | Engineering başı; kodlama ajanı | yüksek |
| Codex | Test yazarı | Uygulama ve testler skills matrix'te Codex'te | yüksek |
| Codex | Hata avcısı (bug finder) | Sandbox içinde okuma ve analiz yapabiliyor | yüksek |
| Codex | Kod inceleyici | Claude/Antigravity koduna çapraz inceleme. Görselleri `view_image` ile de görebiliyor | orta-yüksek |
| Codex | 3D kod üreticisi (yedek, OpenSCAD/Blender script) | Blender Python'u seçerdi ama sandbox salt okunur, dosya yazamıyor ve çalıştıramıyor. Yalnızca script yazar, script'i Antigravity veya Claude çalıştırır | düşük |
| Kimi (BEKLEMEDE) | Çevirmen | Operations: toplu ve ucuz iş; çok dilli metin. Giriş yapılınca test edilmeli | orta (beklemede) |
| Kimi (BEKLEMEDE) | Taslak metin yazarı (toplu) | Çok sayıda varyant üretir (ürün açıklaması, sosyal medya); Claude son halini verir | orta (beklemede) |
| Kimi (BEKLEMEDE) | Dokümantasyon yerelleştirme / düzelti | Teknik yazarın çıktısını çevirir ve dil kontrolü yapar | orta (beklemede) |
| Kimi (BEKLEMEDE) | Veri analisti (hafif) | Toplu CSV/rapor özetleri; ağır işte Claude yedek | düşük (beklemede) |
| Kimi (BEKLEMEDE) | DevOps/CI (yardımcı) | Tekrarlı yapılandırma işleri; yetkinliği bilinmiyor, giriş sonrası değerlendirilir | düşük (beklemede) |

Not: Güvenlik denetçisi, refactoring, performans ve ürün yöneticisi rolleri mühendislik ve operasyon direktörlerinin önerisine bırakıldı. Kreatif taraftan önerim: güvenlik denetçisi Codex'e, refactoring Claude'a gitsin; ama 20 slot sınırı yüzünden tercihi onlara bırakıyorum.

## Kanıt

**Yoklama 1: Antigravity (737 token)**
- Görüntü: Doğrudan bir `generate_image` aracı yok. `invoke_subagent` üzerinden `image-generator` alt ajanının "kayıtlı ve çağrılabilir" olduğunu söylüyor, ama backend'i ya da kotayı canlı olarak doğrulamamış. Sonuç: test edilmeli.
- 3D: Blender Python'u tercih ediyor. Blender 5.1.1'in `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe` yolunda olduğunu söyledi (PATH'te değil). **Yerelde doğrulandı: dosya mevcut.** Node mevcut (doğrulandı). OpenSCAD kurulu değil (doğrulandı: PATH'te yok).
- Görüntü okuma: Var olduğunu söylüyor (`read_file`).

**Yoklama 2: Codex (22.773 token)**
- Görüntü: Yerleşik görüntü üretimi yok (gpt-image yok). Sandbox salt okunur (`sandbox: read-only`), bu yüzden SVG/PNG dosyası bile kaydedemiyor.
- 3D: Blender Python'u tercih ediyor ama sandbox içinde ne çalıştırabiliyor ne de dosya yazabiliyor.
- Görüntü okuma: `view_image` aracı mevcut.

**Claude:** Yerleşik görüntü üretimi yok. Görselleri koddan üretebilir (SVG, Python PIL/matplotlib, three.js, Blender script'i çalıştırarak) ve görüntü dosyalarını Read ile inceleyebilir.

**Kimi:** Giriş yapılmadığı için yoklanmadı.

**Açık testler (test edilmeli):**
1. Antigravity image-generator: küçük bir PNG üretip dosyayı Claude ile açarak kontrol etmek.
2. Antigravity Blender: headless olarak bir küp `.glb` dosyası ve bir render PNG'si üretmek.
3. Codex: yazılabilir sandbox (workspace-write) kullanıcı onayıyla açılırsa SVG/script çıktısını tekrar değerlendirmek.
