# Antigravity CLI Masked Console (Region-Lock Bypass)
🌍 *[Русская версия ниже](#на-русском)*

This repository provides a seamless conversational wrapper for the official **Antigravity CLI** (`agy`). It bypasses strict regional blocks and Google Account endpoint limitations that cause the interactive Terminal User Interface (TUI) to crash or throw `Eligibility check failed` errors.

## The Problem
When accessing the Antigravity CLI from a Datacenter IP (e.g. AWS, DigitalOcean, Datacamp) or an unsupported region, the Google CloudCode API endpoint blocks the UI initialization out of safety and regional compliance. 

```text
⚠ Eligibility Check
  ⎿  Eligibility check failed: Your current account is not eligible 
     for Antigravity, because it is not currently available in your location.
```

## The Solution
`agy` has a built-in headless argument (`--print`). The `--print` argument interacts with the standard inference generation API asynchronously and often entirely bypasses the strict `loadCodeAssist` UI account block. 

This wrapper (`agy-cli.py`) handles:
- Faking a full conversational TUI prompt using raw `stdin/stdout`.
- Stitching conversations gracefully using `--continue` and `--new-project`.
- Fixing `UnicodeDecodeError` issues when interacting via SSH with Cyrillic or other UTF-8 text on varying locales.
- Rapidly injecting explicit VPN / SOCKS5 proxies into the Go backend cleanly.

## Installation

Ensure you have `agy` installed and added to your system `$PATH`, as well as Python 3.

### Windows (Standalone EXE)
You don't need Python to run this on Windows! We automatically build a standalone `.exe` using GitHub Actions.
Simply head over to the **[Actions tab](https://github.com/komu-to/agy-bypass/actions)**, click the latest successful run, and download the `agy-cli-windows` artifact.


```bash
git clone https://github.com/komu-to/agy-bypass.git
cd agy-bypass

# Make it executable and link it globally
chmod +x str_cli.py
sudo ln -s $(pwd)/agy-cli.py /usr/local/bin/agy-cli
```

## Usage

Start the REPL anywhere in your terminal:
```bash
agy-cli
```

### Options
```bash
agy-cli --model "Gemini 3.5 Flash (High)" -y
```
- `-m, --model`: Provide any Antigravity-supported model. Default: `Gemini 3.1 Pro (High)`.
- `-c, --continue-session`: Resume memory from your last closed session.
- `-y, -a, --yes`: Auto-approve all sandbox/permission prompts (injects `--dangerously-skip-permissions`). Required for tools in headless mode.
- `-p, --proxy`: Proxy URL that overrides the default. By default, it looks for `HTTP_PROXY` in the environment.
- `--no-proxy`: Forces direct connection, stripping all injected proxies.

## License
MIT License. Feel free to fork and improve!

---

# На русском

Этот репозиторий содержит удобную консольную обертку для официального приложения **Antigravity CLI** (`agy`). Она позволяет обойти жесткие региональные блокировки (Region Lock) и ограничения аккаунтов Google, из-за которых интерактивный псевдографический интерфейс (TUI) мгновенно закрывается с ошибкой `Eligibility check failed`.

## Проблема
При доступе к Antigravity CLI с IP-адресов дата-центров (VPN, VPS, AWS, Datacamp) или из неподдерживаемых локаций Google API блокирует загрузку рабочего интерфейса в рамках проверки региона.

```text
⚠ Eligibility Check
  ⎿  Eligibility check failed: Your current account is not eligible ...
```

## Решение
Внутри `agy` есть аргумент фонового выполнения (`--print`). Запросы через `--print` уходят в обход проверки аккаунта `loadCodeAssist` для UI, напрямую общаясь с интерфейсом генерации. Эндпоинты генерации проверяют локации гораздо менее строго!

Эта обертка (`agy-cli.py`):
- Полностью имитирует интерактивный чат (REPL), читая и записывая потоки ввода/вывода.
- Сохраняет контекст беседы, используя внутренние аргументы `--continue` и `--new-project`.
- Исправляет падения с `UnicodeDecodeError`, возникающие при нестандартной передаче кириллицы через некоторые SSH-клиенты (работает с сырыми байтами UTF-8).
- Умеет прозрачно "пробрасывать" SOCKS5 и HTTP прокси прямо в процесс Go.

## Установка

Для работы утилиты у вас уже должен быть установлен сам бинарник `agy` и язык Python 3.

### Для пользователей Windows (Автономный EXE)
Вам даже не нужно устанавливать Python! Готовый `.exe` файл собирается автоматически с помощью GitHub Actions.
Перейдите на вкладку **[Actions](https://github.com/komu-to/agy-bypass/actions)**, откройте последнюю сборку и скачайте архив `agy-cli-windows` в самом низу.


```bash
git clone https://github.com/komu-to/agy-bypass.git
cd agy-bypass

chmod +x agy-cli.py
sudo ln -s $(pwd)/agy-cli.py /usr/local/bin/agy-cli
```

## Использование

Просто напишите в терминале:
```bash
agy-cli
```

### Флаги
```bash
agy-cli --model "Gemini 3.5 Flash (High)" -y
```
- `-m, --model`: Позволяет выбрать модель-движок. По умолчанию стартует с `Gemini 3.1 Pro (High)`.
- `-c, --continue-session`: Восстановить контекст и память из последней закрытой сессии.
- `-y, -a, --yes`: Автоматически одобряет все запросы модели на выполнение команд (подставляет флаг `--dangerously-skip-permissions`). Незаменимо для фонового выполнения, где нельзя нажать 'Y'.
- `-p, --proxy`: URL вашего прокси. Если не указано, автоматически ищет системную переменную `HTTP_PROXY` или использует дефолтный адрес.
- `--no-proxy`: Отключает любые прокси, принудительно направляя трафик с нативного интерфейса.

## Лицензия
MIT License. Пользуйтесь и модифицируйте без ограничений!