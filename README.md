<p align="center">
  <img src="icon.png" alt="SMSAPI.pl for Home Assistant" width="150">
</p>

<h1 align="center">SMSAPI.pl for Home Assistant</h1>

<p align="center">
  Wysyłanie wiadomości SMS z Home Assistanta przez polską platformę SMSAPI.pl.
</p>

<p align="center">
  <a href="https://github.com/spec8320/home-assistant-smsapi/releases">
    <img src="https://img.shields.io/github/v/release/spec8320/home-assistant-smsapi?display_name=tag&sort=semver" alt="Latest release">
  </a>
  <a href="https://github.com/spec8320/home-assistant-smsapi/releases">
    <img src="https://img.shields.io/github/downloads/spec8320/home-assistant-smsapi/total" alt="Downloads">
  </a>
  <a href="https://github.com/spec8320/home-assistant-smsapi/issues">
    <img src="https://img.shields.io/github/issues/spec8320/home-assistant-smsapi" alt="Issues">
  </a>
  <a href="https://github.com/spec8320/home-assistant-smsapi/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/spec8320/home-assistant-smsapi" alt="License">
  </a>
  <a href="https://github.com/spec8320/home-assistant-smsapi/commits/main">
    <img src="https://img.shields.io/github/last-commit/spec8320/home-assistant-smsapi" alt="Last commit">
  </a>
  <img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS Custom">
  <img src="https://img.shields.io/badge/Home%20Assistant-2026.3%2B-41BDF5.svg" alt="Home Assistant 2026.3+">
</p>

> [!IMPORTANT]
> Integracja korzysta z płatnej usługi SMSAPI.pl. Każda wysłana wiadomość może wygenerować koszt zgodny z cennikiem Twojego konta SMSAPI.

## 🇵🇱 Polska wersja

### ✨ Funkcje

- konfiguracja w interfejsie Home Assistanta przez **Config Flow**,
- zmiana tokenu, nadawcy i odbiorców przez **Options Flow**,
- standardowa encja `notify`,
- rozszerzona akcja `smsapi.send_sms`,
- obsługa jednego lub wielu odbiorców,
- domyślni odbiorcy zapisani w konfiguracji,
- obsługa zweryfikowanego pola nadawcy SMSAPI,
- opcjonalne usuwanie polskich znaków,
- opcjonalny tryb `fast`,
- diagnostyka z maskowaniem tokenu i numerów telefonu,
- instalacja i aktualizacje przez HACS,
- polskie oraz angielskie tłumaczenia.

---

### 📋 Spis treści

- [Wymagania](#-wymagania)
- [Instalacja przez HACS](#-instalacja-przez-hacs)
- [Instalacja ręczna](#-instalacja-ręczna)
- [Konfiguracja SMSAPI](#-konfiguracja-smsapi)
- [Konfiguracja integracji](#-konfiguracja-integracji)
- [Wysyłanie przez notify](#-wysyłanie-przez-notify)
- [Rozszerzona akcja smsapisend_sms](#-rozszerzona-akcja-smsapisend_sms)
- [Przykładowe automatyzacje](#-przykładowe-automatyzacje)
- [Diagnostyka](#-diagnostyka)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)

---

### ✅ Wymagania

- działająca instalacja Home Assistant,
- HACS — tylko przy instalacji przez HACS,
- aktywne konto w SMSAPI.pl,
- statyczny token OAuth z uprawnieniem do wysyłania wiadomości SMS,
- środki na koncie SMSAPI lub aktywny pakiet,
- opcjonalnie zaakceptowane pole nadawcy w panelu SMSAPI.

---

### 📦 Instalacja przez HACS

#### Dodanie jako Custom Repository

1. Otwórz **HACS → Integrations**.
2. Kliknij menu z trzema kropkami.
3. Wybierz **Custom repositories**.
4. Dodaj adres:

   ```text
   https://github.com/spec8320/home-assistant-smsapi
   ```

5. Wybierz kategorię **Integration**.
6. Wyszukaj **SMSAPI.pl** i kliknij **Download**.
7. Uruchom ponownie Home Assistant.
8. Przejdź do:

   ```text
   Ustawienia → Urządzenia i usługi → Dodaj integrację
   ```

9. Wyszukaj **SMSAPI.pl**.

---

### 📁 Instalacja ręczna

1. Pobierz najnowsze wydanie projektu.
2. Skopiuj katalog:

   ```text
   custom_components/smsapi
   ```

   do katalogu Home Assistanta:

   ```text
   /config/custom_components/smsapi
   ```

3. Sprawdź, czy istnieje plik:

   ```text
   /config/custom_components/smsapi/manifest.json
   ```

4. Uruchom ponownie Home Assistant.
5. Dodaj integrację z poziomu interfejsu.

---

### 🔑 Konfiguracja SMSAPI

W panelu SMSAPI utwórz **statyczny token OAuth** z uprawnieniem pozwalającym wysyłać SMS-y.

> [!CAUTION]
> Nie dodawaj tokenu do repozytorium, logów, screenów ani zgłoszeń GitHub Issues.

Numery telefonu najlepiej zapisywać w formacie międzynarodowym:

```text
48500100200
```

Dopuszczalny jest również zapis z plusem:

```text
+48500100200
```

Pole nadawcy, np. `MojDom`, musi być wcześniej zaakceptowane na koncie SMSAPI.

---

### ⚙️ Konfiguracja integracji

Podczas dodawania integracji podajesz:

| Pole | Wymagane | Opis |
|---|:---:|---|
| Token OAuth | ✅ | Statyczny token API wygenerowany w SMSAPI |
| Domyślne pole nadawcy | ❌ | Zweryfikowana nazwa nadawcy, maksymalnie 11 znaków |
| Domyślni odbiorcy | ❌ | Numery rozdzielone przecinkami |

Ustawienia można później zmienić bez usuwania integracji:

```text
Ustawienia → Urządzenia i usługi → SMSAPI.pl → Konfiguruj
```

---

### 💬 Wysyłanie przez `notify`

Po skonfigurowaniu integracji Home Assistant utworzy encję powiadomień, zazwyczaj podobną do:

```text
notify.smsapi_pl
```

Dokładny identyfikator sprawdź w interfejsie Home Assistenta.

```yaml
action: notify.send_message
target:
  entity_id: notify.smsapi_pl
data:
  title: "Alarm"
  message: "Wykryto ruch w garażu."
```

Ta metoda korzysta z domyślnego nadawcy i domyślnych odbiorców zapisanych w konfiguracji.

---

### 📨 Rozszerzona akcja `smsapi.send_sms`

Użyj jej, gdy chcesz dynamicznie wybrać odbiorców albo użyć parametrów specyficznych dla SMSAPI.

```yaml
action: smsapi.send_sms
data:
  recipients:
    - "48500100200"
    - "48500200300"
  sender: "MojDom"
  message: "ALARM! Otwarto drzwi wejściowe."
  normalize: true
  fast: false
```

#### Parametry akcji

| Parametr | Wymagany | Typ | Opis |
|---|:---:|---|---|
| `message` | ✅ | string | Treść wiadomości |
| `recipients` | ❌ | lista | Numery odbiorców; bez pola używane są numery domyślne |
| `sender` | ❌ | string | Pole nadawcy; bez pola używany jest nadawca domyślny |
| `normalize` | ❌ | boolean | Zamiana polskich znaków na znaki podstawowe |
| `fast` | ❌ | boolean | Wysyłka z parametrem `fast=1` |

---

### 🚨 Przykładowe automatyzacje

Gotowe pliki znajdują się również w katalogu [`examples`](examples).

<details>
<summary><strong>Alarm — wykrycie ruchu w garażu</strong></summary>

```yaml
alias: SMS - alarm garaż
triggers:
  - trigger: state
    entity_id: binary_sensor.ruch_garaz
    to: "on"

conditions:
  - condition: state
    entity_id: alarm_control_panel.alarm_dom
    state:
      - armed_away
      - armed_night

actions:
  - action: notify.send_message
    target:
      entity_id: notify.smsapi_pl
    data:
      title: "ALARM"
      message: >-
        Wykryto ruch w garażu.
        Czas: {{ now().strftime('%d.%m.%Y %H:%M:%S') }}

mode: single
```

</details>

<details>
<summary><strong>Brama pozostawiona otwarta przez 10 minut</strong></summary>

```yaml
alias: SMS - otwarta brama
triggers:
  - trigger: state
    entity_id: binary_sensor.brama_wjazdowa
    to: "on"
    for: "00:10:00"

actions:
  - action: smsapi.send_sms
    data:
      message: >-
        Uwaga! Brama wjazdowa jest otwarta od co najmniej 10 minut.
      normalize: true

mode: restart
```

</details>

<details>
<summary><strong>Pralka zakończyła pracę</strong></summary>

```yaml
alias: SMS - pralka zakończyła pracę
triggers:
  - trigger: numeric_state
    entity_id: sensor.pralka_power
    below: 3
    for: "00:03:00"

actions:
  - action: notify.send_message
    target:
      entity_id: notify.smsapi_pl
    data:
      message: "Pralka zakończyła pracę."

mode: single
```

</details>

<details>
<summary><strong>UPS pracuje na baterii</strong></summary>

```yaml
alias: SMS - UPS na baterii
triggers:
  - trigger: state
    entity_id: binary_sensor.ups_on_battery
    to: "on"

actions:
  - action: smsapi.send_sms
    data:
      recipients:
        - "48500100200"
      message: >-
        Awaria zasilania. UPS przeszedł na baterię.
        Poziom: {{ states('sensor.ups_battery_charge') }}%.

mode: single
```

</details>

---

### 🩺 Diagnostyka

Diagnostykę można pobrać z menu integracji w Home Assistant.

Integracja maskuje:

- token OAuth,
- listę numerów odbiorców.

Diagnostyka pokazuje między innymi:

- stan wpisu konfiguracyjnego,
- informację, czy ustawiono nadawcę,
- liczbę skonfigurowanych odbiorców,
- informację, czy token został ustawiony.

Mimo maskowania zawsze przejrzyj plik przed opublikowaniem go w zgłoszeniu.

---

### 🛠 Rozwiązywanie problemów

#### Integracja nie pojawia się po instalacji

1. Sprawdź strukturę katalogów:

   ```text
   /config/custom_components/smsapi/manifest.json
   ```

2. Uruchom ponownie Home Assistant.
3. Wyczyść pamięć podręczną przeglądarki lub użyj `Ctrl+F5`.
4. Sprawdź **Ustawienia → System → Dzienniki**.

#### `Invalid handler specified`

Najczęściej oznacza błąd ładowania `config_flow.py`.

- upewnij się, że używasz najnowszego wydania,
- wykonaj ponowne pobranie integracji w HACS,
- uruchom ponownie cały Home Assistant,
- sprawdź pełny wyjątek dotyczący `custom_components.smsapi`.

#### Błąd autoryzacji lub HTTP 401/403

- wygeneruj nowy statyczny token OAuth,
- sprawdź uprawnienie do wysyłki SMS,
- usuń przypadkowe spacje przed lub po tokenie,
- zaktualizuj token przez opcję **Konfiguruj**.

#### Wiadomość nie ma własnego nadawcy

Pole nadawcy musi być wcześniej zaakceptowane przez SMSAPI. Bez niego SMSAPI może użyć domyślnego nadawcy dostępnego na koncie.

#### SMS jest dłuższy lub droższy niż oczekiwano

Polskie znaki mogą zmniejszyć liczbę znaków mieszczących się w pojedynczym SMS-ie. Użyj:

```yaml
normalize: true
```

---

### 🤝 Zgłaszanie błędów i współpraca

Zgłoszenia i propozycje zmian są mile widziane w sekcji GitHub Issues.

Przed zgłoszeniem:

1. zaktualizuj integrację,
2. uruchom ponownie Home Assistant,
3. sprawdź logi,
4. usuń tokeny i numery telefonów,
5. dołącz bezpieczną diagnostykę.

---

## 🇬🇧 English version

### Overview

SMSAPI.pl for Home Assistant is a custom integration that sends SMS notifications through the Polish SMSAPI.pl platform.

### Features

- UI-based Config Flow,
- editable Options Flow,
- standard Home Assistant notify entity,
- extended `smsapi.send_sms` action,
- multiple recipients,
- configurable sender name,
- optional character normalization,
- optional SMSAPI fast mode,
- redacted diagnostics,
- HACS-compatible installation and updates.

### Installation using HACS

1. Open **HACS → Integrations**.
2. Add this repository as a custom integration repository:

   ```text
   https://github.com/spec8320/home-assistant-smsapi
   ```

3. Install **SMSAPI.pl**.
4. Restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration**.
6. Search for **SMSAPI.pl**.

### Manual installation

Copy:

```text
custom_components/smsapi
```

to:

```text
/config/custom_components/smsapi
```

Restart Home Assistant and add the integration from the UI.

### Sending a notification

```yaml
action: notify.send_message
target:
  entity_id: notify.smsapi_pl
data:
  title: "Alarm"
  message: "Motion detected in the garage."
```

### Extended action

```yaml
action: smsapi.send_sms
data:
  recipients:
    - "48500100200"
  sender: "MyHome"
  message: "Alarm! The front door was opened."
  normalize: true
  fast: false
```

### Security

Never publish your OAuth token or complete phone numbers. The diagnostics module redacts the token and recipient list, but you should still review diagnostic files before sharing them.

---

## 📜 Licencja / License

Projekt jest udostępniony na licencji [MIT](LICENSE).

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made for Home Assistant users using SMSAPI.pl
</p>
