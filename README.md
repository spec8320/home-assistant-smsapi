# SMSAPI.pl for Home Assistant

Custom integration for sending SMS messages through [SMSAPI.pl](https://www.smsapi.pl/).

## Features

- configuration from the Home Assistant UI,
- modern `notify` entity,
- extended `smsapi.send_sms` action,
- multiple recipients,
- configurable sender name,
- optional Polish-character normalization,
- HACS installation and updates,
- HACS and Hassfest validation workflows.

## Repository

GitHub: `https://github.com/spec8320/home-assistant-smsapi`

Manual, owner-specific follow-up work is tracked in [`TODO.md`](TODO.md).

## Installation through HACS as a custom repository

1. Publish this project as a **public GitHub repository**.
2. In HACS open **Integrations**.
3. Open the menu and select **Custom repositories**.
4. Enter your repository URL.
5. Select category **Integration**.
6. Install **SMSAPI.pl** and restart Home Assistant.
7. Go to **Settings → Devices & services → Add integration → SMSAPI.pl**.

## SMSAPI token

Generate a static OAuth token in the SMSAPI customer panel. It needs permission to send SMS messages.
Never put the token in GitHub, screenshots, logs or issue reports.

## Standard notify entity

After setup, Home Assistant creates a notify entity, normally:

```text
notify.smsapi_pl
```

Use the entity picker rather than relying on the exact entity ID.

```yaml
action: notify.send_message
target:
  entity_id: notify.smsapi_pl
data:
  title: "Alarm"
  message: "Wykryto ruch w garażu."
```

The notify entity sends messages to recipients configured in the integration.

## Extended action

To select recipients dynamically or use SMSAPI-specific options:

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

## Example alarm automation

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

## Publishing a release

1. Change `version` in `custom_components/smsapi/manifest.json`.
2. Commit and push.
3. Ensure **HACS validation** and **Hassfest** pass.
4. Create a GitHub Release with a tag matching the manifest, e.g. `v1.2.0`.
5. The release workflow automatically creates and uploads `smsapi.zip`.

## Adding to the default HACS catalog

First make the repository publicly available and verify that both validation workflows pass.
Then publish a full GitHub Release and submit the repository to the HACS default repository list.

## Security

Phone numbers and SMS contents can be sensitive. Sanitize diagnostic logs before publishing them.
SMS sending may incur charges on your SMSAPI account.

## License

MIT


## Changing settings

Open **Settings → Devices & services → SMSAPI.pl → Configure**.
The options flow lets you update the OAuth token, sender and recipients without removing the integration.

## Diagnostics

Safe diagnostics are available from the integration menu. The OAuth token and recipient list are redacted.
Always review downloaded diagnostics before publishing them.
