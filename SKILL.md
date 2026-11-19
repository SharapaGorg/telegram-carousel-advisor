---
name: "telegram-carousel"
description: "Делает карусель для Telegram-канала Writelo: альбом до 10 квадратных слайдов PNG 1080×1080 в фирменном стиле плюс подпись до 1024 символов. Для просьб «сделай карусель для телеги»."
---

# Карусель для Telegram (Writelo)

## Что такое карусель в Telegram
Свайпа как в Instagram в Telegram нет. Карусель выкладывается **альбомом (медиагруппой)**:
- до **10** изображений, в ленте они показываются сеткой, по тапу открываются на весь экран и листаются;
- первый слайд в сетке самый крупный, поэтому на нём должен быть хук;
- подпись к альбому до **1024 символов** (лимит подписи к медиа без Premium), она висит под сеткой;
- формат для Telegram: **квадрат 1080×1080**, только статичные картинки, без видео и анимаций;
- для Instagram-карусели тот же контент делается отдельно в 1080×1350 (4:5), и там большинство слайдов должны быть видео (скринкасты или анимации), это помогает продвижению.

## Чистый стиль (по умолчанию для Telegram)
Готовый шаблон лежит в репозитории SharapaGorg/telegram-carousel-advisor: `templates/clean-square.html` и `render.py`. Чем он отличается от «терминального» стиля ниже:
- ровный фон ink `#0E0D0C` без сетки, сканлайнов и cyan-тени, только мягкое оранжевое свечение в правом нижнем углу;
- сверху вордмарк `WRITELO` (Unbounded 700, разрядка .12em, оранжевая точка) и счётчик `02 / 08`, внизу нет «листай →»;
- над заголовком номер пункта `01 ——` оранжевым моно; заголовок Unbounded 900 80px капсом, акцент просто оранжевым; лид JetBrains Mono 34px;
- в нижней половине каждого слайда один простой визуальный элемент: столбики сравнения, купоны промокодов, строка поиска, плитки ✓/×;
- источники цифр мелкой сноской 21px ash внизу слайда.

## Факты для сравнения с Trendsee (проверено 19.11.2026)
- Writelo «Нос по ветру»: 699 ₽/мес, 1 667 ₽ за 3 месяца, 5 000 ₽/год; 250 анализов видео в месяц, 20 аккаунтов конкурентов, ежедневно 100 рилсов, отобранных командой (writelo.io).
- Writelo Free: поиск по смыслу и фильтры, в выдаче первые 6 роликов, 5 анализов видео, 1 разбор аккаунта. Промокод «ПУСК»: −25% новым пользователям. Отмена автопродления в профиле (writelo.io/terms, п. 4.6).
- Trendsee «Аналитика контента»: 3 300 ₽/мес, при оплате за год 2 640 ₽/мес, 2 500 токенов; Visioner 15 800 ₽/мес (trendsee.io/it-product). Ролики собирает алгоритм (trendsee.io). Около 180 разборов на 2 500 токенов: это из статьи на vc.ru, у самого Trendsee такой цифры нет.
- Временные акции (например «ЛУЧШИЕ» −30% до конца ноября 2026) берём только со слов Егора и проверяем, не истекли ли.

## Порядок работы
1. **Материал.** Берём тему и факты у пользователя: текст, ролик, описание, прошлые посты. Если есть похожий прошлый пост или ролик, ищем его в истории чатов и не переспрашиваем.
2. **Проверка фактов до вёрстки.** Цифры, названия, чьи это продукты: каждое утверждение должно опираться на слова пользователя или на открытый источник. Ничего не додумываем. В октябрьской карусели я приписал Radolyn Labs продукты для FunPay и «10+ лет вместе», подтверждения не было, пришлось убирать. Если факт не подтверждён, лучше переформулировать или спросить.
3. **Структура (5–8 слайдов, максимум 10):**
   - 1: обложка, только хук с обещанием, ради чего листать. Пункты на обложке НЕ перечисляем: список убивает интригу, их раскрывают следующие слайды;
   - 2…N−1: на каждом слайде одна мысль, крупный заголовок плюс 1–3 строки пояснения или плашки/цифры;
   - N: финал с CTA (writelo.io, «пишите в комментарии»), без «листай →».
   Текст на слайде короткий: заголовок до ~3 строк, тело до ~4 строк. Всё, что не влезает, уходит в подпись.
4. **Вёрстка:** один `slides.html`, каждый слайд в `<section class="slide">` (шаблон ниже).
5. **Рендер** скриптом `render.py`, PNG получаются в `out/slide-NN.png`.
6. **Визуальная проверка.** Склеиваем контактный лист и смотрим глазами: не вылез ли текст, не наехал ли на HUD или подвал, читается ли шрифт на телефоне:
   ```bash
   N=$(ls out/slide-*.png | wc -l); ffmpeg -v error -y $(for f in out/slide-*.png; do echo -n "-i $f "; done) -filter_complex "$(for i in $(seq 0 $((N-1))); do echo -n "[$i]scale=360:-1[s$i];"; done)$(for i in $(seq 0 $((N-1))); do echo -n "[s$i]"; done)hstack=$N" out/sheet.png
   ```
   Ключевые слайды смотрим крупнее (scale=540). Правим, рендерим заново, снова проверяем.
7. **Сдача.** Все PNG отправляем через SendUserFile одним вызовом, по порядку. В ответе: краткий список слайдов (номер и одна строка), готовая подпись к альбому в блоке кода (≤1024 символов, посчитать `len()`), отдельной строкой что из фактов откуда взято и что я убрал как неподтверждённое.

## Точки в конце
Никогда не ставим точку в конце последнего предложения: ни на слайдах (заголовки, лиды, сноски, плашки), ни в подписи (в конце абзацев и пунктов списка). Точки внутри текста между предложениями остаются.

## Подпись к альбому
- Первая строка — хук, видна в превью.
- Голос Егора, от первого лица, живой и без канцелярита. Без размытых фраз вроде «теперь всё это в Writelo»: функционал перечисляем конкретно.
- Функции Writelo нумерованным списком, если они к месту.
- В конце CTA: writelo.io и/или вопрос в комментарии.

## Стиль Writelo
Тёмный «терминальный» стиль, как на обложках роликов.
- Цвета: ink `#0A0A0A` (фон), paper `#EDE8DE` (текст), orange `#D4683F` (акцент), cyan `#3FD0E0` (глитч-тень акцента), ash `#A8A094` (второстепенный), char `#3A3530` (рамки).
- Шрифты: **Unbounded 900** для заголовков (капсом, letter-spacing −0.04em), **JetBrains Mono** для текста и HUD.
- Фон: сетка 80px, оранжевое свечение снизу, сканлайны.
- HUD сверху: оранжевая точка + метка раздела слева, счётчик `01 / 07` справа. Подвал: `writelo.io` слева, `листай →` справа (на последнем слайде без него).
- Акцентное слово: оранжевое с cyan-тенью `5px 0`. Плашки-чипы: обводка char, «горячая» плашка залита оранжевым. Большие цифры: Unbounded оранжевым.
- Отступы по краям 64px, текст не ближе 40px к краю.
- Иллюстраций (человечки Егора и Завара, логотип AyuGram) в этом окружении нет: они остались в октябрьском проекте Remotion. Если нужны, просим SVG или PNG у пользователя, сами не рисуем похожие.

## Окружение и рендер
Chrome лежит в `/usr/bin/google-chrome`, Python Playwright установлен. Шрифты ставим из npm:
```bash
mkdir -p carousel && cd carousel && npm init -y >/dev/null && npm i @fontsource/unbounded @fontsource/jetbrains-mono
```

`render.py`:
```python
import sys, pathlib
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "slides.html").resolve()
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "out"); out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
    pg.goto(src.as_uri()); pg.evaluate("document.fonts.ready")
    slides = pg.query_selector_all("section.slide")
    for i, s in enumerate(slides, 1):
        s.screenshot(path=str(out / f"slide-{i:02d}.png"))
        over = s.evaluate("""el => [...el.querySelectorAll('*')].filter(n => {
            const r = n.getBoundingClientRect(), R = el.getBoundingClientRect();
            return n.children.length === 0 && n.textContent.trim() && (r.right > R.right - 40 || r.bottom > R.bottom - 40 || r.left < R.left + 40);
        }).map(n => n.textContent.trim().slice(0, 40))""")
        if over: print(f"slide {i}: близко к краю/вылезает -> {over}")
    print(f"rendered {len(slides)} slides"); b.close()
```
Запуск: `python3 render.py slides.html out`. Предупреждения о краях исправляем обязательно.

## Шаблон slides.html
```html
<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:UNB;font-weight:900;src:url(node_modules/@fontsource/unbounded/files/unbounded-cyrillic-900-normal.woff2)}
@font-face{font-family:UNB;font-weight:900;src:url(node_modules/@fontsource/unbounded/files/unbounded-latin-900-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:MONO;src:url(node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-cyrillic-400-normal.woff2)}
@font-face{font-family:MONO;src:url(node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2);unicode-range:U+0000-00FF}
@font-face{font-family:MONO;font-weight:700;src:url(node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-cyrillic-700-normal.woff2)}
:root{--ink:#0A0A0A;--paper:#EDE8DE;--orange:#D4683F;--ash:#A8A094;--cyan:#3FD0E0;--char:#3A3530}
body{margin:0;background:#222}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;background:var(--ink);color:var(--paper);font-family:MONO}
.slide::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(237,232,222,.07) 2px,transparent 2px),linear-gradient(90deg,rgba(237,232,222,.07) 2px,transparent 2px);background-size:80px 80px}
.slide::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(0deg,rgba(212,104,63,.6),rgba(212,104,63,.18) 22%,transparent 45%),repeating-linear-gradient(0deg,rgba(237,232,222,.035) 0 2px,transparent 2px 5px)}
.hud,.foot{position:absolute;left:64px;right:64px;display:flex;justify-content:space-between;font-size:28px;letter-spacing:.08em;color:var(--ash);z-index:2}
.hud{top:56px}.foot{bottom:52px}
.hud b{color:var(--paper);font-weight:400;display:flex;align-items:center;gap:14px}
.hud b::before{content:"";width:18px;height:18px;border-radius:9px;background:var(--orange)}
.body{position:absolute;left:64px;right:64px;top:170px;z-index:2}
h1{font-family:UNB;font-weight:900;font-size:96px;line-height:1.02;letter-spacing:-.04em;margin:0}
.acc{color:var(--orange);text-shadow:5px 0 var(--cyan)}
.kicker{font-size:34px;color:var(--orange);margin-bottom:20px}
p{font-size:38px;line-height:1.45}
.big{font-family:UNB;font-weight:900;font-size:116px;letter-spacing:-.05em;color:var(--orange);text-shadow:6px 0 var(--cyan)}
.chips{display:flex;flex-wrap:wrap;gap:18px}
.chip{padding:10px 18px 12px;border:3px solid var(--char);font-weight:700;font-size:32px}
.chip.hot{background:var(--orange);border-color:var(--orange);color:var(--ink)}
</style></head><body>
<section class="slide">
  <div class="hud"><b>МЕТКА</b><span>01 / 07</span></div>
  <div class="body">
    <div class="kicker">&gt; подзаголовок</div>
    <h1>ЗАГОЛОВОК<br><span class="acc">АКЦЕНТ</span></h1>
    <p>Короткое пояснение.</p>
  </div>
  <div class="foot"><span>writelo.io</span><span style="color:var(--paper)">листай →</span></div>
</section>
<!-- следующие слайды -->
</body></html>
```
Если заголовок не влезает, уменьшаем `font-size` у h1 на конкретном слайде (78–92px), а не режем отступы.

## Не делать
- Не выдумывать цифры, достижения и атрибуции.
- Не рисовать чужих персонажей и логотипы, только присланные пользователем файлы.
- Не делать больше 10 слайдов: Telegram не пропустит альбом.