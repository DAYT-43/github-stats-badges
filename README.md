# github-stats-badges

> README репозитория `github-stats-badges`. ЧЕРНОВИК — ждёт подтверждения пользователя (правило «Сначала Obsidian — потом GitHub»).
>
> 🎯 Кликбейт-заголовок (предлагается): **«Твой GitHub-профиль врёт о тебе. Покажи ЧЕСТНУЮ статистику»**.
>
> 📊 **Статус 2026-08-15:** карточка проекта создана (draft), скрипт и workflow готовы и протестированы (Stars=14, Contributions=31). Ждёт подтверждения публикации.

## Описание

**Сколько на самом деле звёзд у твоих проектов? Сколько контрибуций ты сделал за год?** Популярные виджеты (`github-readme-stats` и др.) считают только публичные репозитории, падают при rate-limit и показывают календарный год (сбрасываются в январе).

Этот проект показывает **честную статистику** профиля GitHub в виде автообновляемых бейджей, построенных на официальных API GitHub:

- ⭐ **Stars earned** — сумма звёзд на всех публичных репозиториях (REST API).
- 📈 **Contributions (last year)** — контрибуции за скользящие 365 дней (GraphQL API) — ровно то, что GitHub показывает на твоём профиле.

Бейджи генерируются в `badge.json` (schema shields.io endpoint) и обновляются раз в день через GitHub Actions — единый стиль с остальными бейджами профиля.

⭐ **Понравилась идея? Поставь звезду** — это лучшая благодарность автору и сигнал GitHub, что проект полезен.
🍴 **Хочешь свою версию? Форкни репозиторий** — всё для этого уже готово (инструкция ниже).
💡 **Есть идея улучшения? Открой Issue или Pull Request** — автор активно дорабатывает проект и отвечает на предложения.

## Почему это интересно (ход мысли)

1. **Проблема виджетов**: `github-readme-stats` (79.7k ⭐) — самый популярный, но: считает только публичные репозитории, живёт на общих Vercel-инстансах (rate-limit → битые картинки), а «contributions» показывает за календарный год (сбрасывается в январе).
2. **Открытие — GraphQL API**: `contributionsCollection.contributionCalendar.totalContributions` отдаёт контрибуции за **скользящие 365 дней** — то, что GitHub показывает на самом профиле. REST такого не умеет.
3. **Stars — REST API**: `GET /users/{owner}/repos?per_page=100` → сумма `stargazers_count` (с пагинацией).
4. **Единый паттерн**: тот же, что в `unique-visitors-badge` — GitHub Actions раз в день снимает данные, генерирует `badge.json`, бейдж вставляется в README профиля.
5. **Честность**: данные из официального API, без сторонних сервисов и «накрутки».

## Установка / Запуск

Для владельца профиля (скопировать в свой аккаунт):

1. Создать репозиторий `github-stats-badges` (или форкнуть этот).
2. Добавить секрет **`GH_TOKEN`** в `Settings → Secrets and variables → Actions` — PAT с доступом к аккаунту (для GraphQL нужен скоуп `read:user` или `repo`).
3. Скопировать файлы: `.github/workflows/update-stats.yml`, `scripts/update_stats.py`.
4. Указать свой аккаунт в настройках workflow/скрипта (переменная `OWNER`).
5. В README профиля добавить бейджи:

```markdown
![Stars earned](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/OWNER/github-stats-badges/main/stars.json)
![Contributions](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/OWNER/github-stats-badges/main/contributions.json)
```

Запуск:

```bash
# ручной запуск workflow из Actions → Update profile stats badges → Run workflow
# либо дождаться ежедневного cron (по расписанию)
```

## Структура проекта

```
github-stats-badges/
├── .github/
│   └── workflows/
│       └── update-stats.yml      # ежедневный cron + workflow_dispatch
├── scripts/
│   └── update_stats.py           # сбор REST + GraphQL + генерация badge.json
├── stars.json                    # сгенерированные данные для shields.io endpoint
├── contributions.json            # сгенерированные данные для shields.io endpoint
├── README.md
└── LICENSE
```

## Решения (ADR-lite)

| Проблема | Решение | Почему |
|---|---|---|
| Виджеты считают только публичные репо и падают от rate-limit | Собственный сбор через официальный API | Честные данные, полный контроль, нет зависимости от чужих сервисов |
| REST не отдаёт контрибуции за скользящий год | GraphQL `contributionsCollection` | Ровно то, что GitHub показывает на профиле (365 дней), не календарный год |
| Stars по всем репозиториям | REST `users/{owner}/repos` + пагинация | Простая и надёжная сумма `stargazers_count` |
| Единый стиль бейджей профиля | shields.io endpoint badge | `img.shields.io/endpoint?url=badge.json` — тот же стиль, что и остальные бейджи |
| Доступ к API | Секрет `GH_TOKEN` (PAT) | Токен не попадает в логи и не публикуется в репозитории |

## Стек

- Python — скрипт сбора и генерации `badge.json`
- GitHub Actions — расписание (cron) + ручной запуск (`workflow_dispatch`)
- GitHub REST API — `users/{owner}/repos` (stars)
- GitHub GraphQL API — `contributionsCollection` (contributions)
- shields.io — endpoint badge
- JSON — хранение данных и обмен с shields.io
- git — версионирование и публикация

## Лицензия

MIT

## Контакты

Дмитрий (DAYT-43) — https://github.com/DAYT-43

---

### 🚀 Помоги проекту стать лучше

1. ⭐ **Поставь звезду** — так проект увидят больше людей и автор получит заслуженную обратную связь.
2. 🍴 **Форкни** — у тебя будет своя копия, в которой можно менять всё что угодно.
3. 💡 **Предложи улучшение**: идея, баг, новая фича — открывай Issue или Pull Request. Автор отвечает и дорабатывает.

Спасибо, что заглянул! 🙌
