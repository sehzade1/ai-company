# Mühendislik Direktörü Önerisi: İşçi Ajan Kadrosu (20 rol)

Bakış açısı: kod kalitesi, testler, hatalar, güvenlik. Temel kural: aynı türdeki işin yazarı ve gözden geçireni aynı modelde olmaz (çapraz inceleme).

## Kanıt (tek Codex yoklaması, öz-beyan verisi, doğrulanmadı)
- Codex (gpt-6-luna) kendini en güçlü saydığı alanlar: backend kod analizi, hata bulma, refactoring, test yazma, frontend kod analizi/düzenleme.
- En zayıf saydığı alanlar: servis çalıştırma/deploy gerektiren DevOps, görsel iterasyon isteyen 3D işi, görsel üretimi.
- Kısıt: mevcut sandbox **salt-okunur**, ağ kısıtlı. Dosya yazamıyor, build/test çalıştıramıyor. Yazar rolleri bu yüzden ya yama (diff) üretir ve Claude uygular, ya da kullanıcı onayıyla yazma izinli sandbox açılır. **Test edilmeli.**
- Yoklama maliyeti: 4.392 token (Codex günlük 8.611/500.000, %1,7).

## Atama tablosu

| Model | Rol | Gerekçe | Güven |
|---|---|---|---|
| Claude | Kod gözden geçirici (code reviewer) | Codex backend'ini ve Antigravity frontend'ini inceler; kendi yazdığı kod yok, bu yüzden çapraz kural sağlanıyor | high |
| Claude | Güvenlik denetçisi | Tam araç erişimi var: bağımlılık taraması çalıştırabilir, istismarı yeniden üretebilir. Yazar olarak Codex ve Antigravity'yi denetler | high |
| Claude | Test yazarı | Testleri gerçekten çalıştırabilen tek aktif model (Codex sandbox'ı çalıştıramıyor). Testlerin Codex backend'inden ayrı bir modelde yazılması kör noktaları azaltır | high |
| Claude | DevOps/CI | Komut çalıştırma ve dosya yazma gerektiriyor. Codex bunu zayıf yanı olarak kendisi söyledi. CI yapılandırmasını Codex (bug finder) inceler | medium |
| Claude | Erişilebilirlik denetçisi | Antigravity'nin frontend ve UI işini başka bir model incelemiş olur. Tarayıcı aracıyla gerçek DOM kontrolü yapılabilir | medium |
| Codex | Backend geliştirici | Öz-beyanda en güçlü alan, gerçek token sayımı var. İncelemeyi Claude yapar, testleri Claude yazar | high |
| Codex | Refactoring uzmanı | Öz-beyanda güçlü. Davranış korunmasını Claude'un testleri doğrular | high |
| Codex | Hata avcısı (bug finder) | Öz-beyanda güçlü. Yalnızca başka modellerin kodunda (Antigravity frontend/3D, Claude CI, Kimi script'leri) çalışır, Codex backend'inde çalışmaz | medium |
| Codex | Performans optimizasyoncusu | Kod analizi güçlü, ancak ölçüm (profiling) çalıştıramıyor. Benchmark'ı Claude koşar. Test edilmeli | medium |
| Codex | Veri analisti | Python/SQL analiz kodu yazmak koda yakın bir iş. Sandbox'ta veriye erişip erişemediği test edilmeli | low |
| Antigravity | Frontend geliştirici | Gemini'nin çok kipli (multimodal) yapısı UI'ya uygun. Kod incelemesini Claude, hata avını Codex, erişilebilirlik denetimini Claude yapar. Kod kalitesi test edilmeli | medium |
| Antigravity | UI/UX tasarımcı | Görsel girdiyi değerlendirebilir. Tasarım çıktısını uygulayan da Antigravity olduğu için tasarımı Claude (erişilebilirlik) inceler | medium |
| Antigravity | 3D modelci (Blender Python / three.js / OpenSCAD) | Render görüntüsüne bakıp iterasyon yapabilmesi bekleniyor, Codex ise bunu zayıf yanı olarak belirtti. Kodu Codex hata avcısı inceler. `agy -p` ile görsel geri bildirim döngüsü test edilmeli | low |
| Antigravity | Görsel üretici | Google ekosistemi bunu mümkün kılabilir, ancak `agy -p` CLI'ının görsel dosya üretip üretemediği bilinmiyor. Test edilmeli | low |
| Antigravity | Araştırmacı | ORG'da Research başkanı, uzun bağlam ve web desteği var. İddialarını Claude kaynak kontrolüyle doğrular | high |
| Kimi (PENDING LOGIN) | Teknik yazar | Doküman ve README taslakları hacimli ve ucuz iş. Teknik doğruluğu Claude code reviewer kontrol eder | low |
| Kimi (PENDING LOGIN) | Çevirmen | ORG'da Operations, çeviri ve toplu iş için tanımlı. Örneklemeyle Antigravity kontrol eder | low |
| Kimi (PENDING LOGIN) | Metin yazarı (copywriter) | Taslak üretimi ucuz ve hacimli. Marka ve ton kontrolü yaratıcı ekipte kalır | low |
| Kimi (PENDING LOGIN) | Prompt mühendisi | Diğer ajanlar için görev şablonları yazar. Şablonları çalıştıran modeller çıktıyı sınar. Test edilmeli | low |
| Kimi (PENDING LOGIN) | Ürün yöneticisi | Spec ve backlog taslağı çıkarır. Nihai karar CEO'da kalır, teknik fizibiliteyi Mühendislik onaylar | low |

## Çapraz inceleme eşleşmeleri (yazar → inceleyen)
- Backend/refactor/performans (Codex) → kod incelemesi, test ve güvenlik (Claude)
- Frontend/UI/3D (Antigravity) → hata avı (Codex), kod incelemesi ve erişilebilirlik (Claude)
- DevOps/CI (Claude) → hata avı (Codex)
- Testler (Claude) → Codex hata avcısı test kapsamı boşluklarını işaretler
- Doküman/çeviri/prompt (Kimi) → teknik doğruluk (Claude), çeviri örneklemesi (Antigravity)
- Araştırma (Antigravity) → kaynak doğrulama (Claude)

## Riskler ve açık noktalar
1. Claude'da beş inceleme ve altyapı rolü toplanıyor, bu da bir darboğaz riski. Finans, Claude yükünü izlemeli. Yedek inceleyici Codex olabilir, ama Codex'in yazdığı kod hariç.
2. Codex'in sandbox'ı salt-okunur olduğundan yazar rolleri yama üretir. Yazma izni yalnızca kullanıcının açık onayıyla verilebilir.
3. Kimi giriş yapana kadar 5 rol boşta kalıyor. Geçici yedekler: teknik yazar Claude, çeviri Antigravity, diğerleri Antigravity veya Claude. Bu durumda çapraz kural yeniden kontrol edilmeli.
4. "Test edilmeli" ile işaretli bütün atamalar ilk gerçek görevden sonra roster'daki performans notlarına göre yeniden değerlendirilmeli.
