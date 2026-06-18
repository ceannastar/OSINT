export const SUGGESTIONS = [
  {
    svgIcon: '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22 6 12 13 2 6"/>',
    title: 'Исследовать Email адрес',
    prompt: 'Чтобы исследовать Email адрес, попросите меня об этом',
  },
  {
    svgIcon: '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    title: 'Проверить username',
    prompt: 'Чтобы исследовать username в социальных сетях, попросите меня об этом',
  },
  {
    svgIcon: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    title: 'Проанализировать IP-адрес',
    prompt: 'Чтобы исследовать IP-адрес, попросите меня об этом',
  },
  {
    svgIcon: '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>',
    title: 'Проверка домена',
    prompt: 'Чтобы собрать информацию о домене, попросите меня об этом',
  },
]

export const API_KEYS = [
  { key: 'HIBP_API_KEY',        label: 'HaveIBeenPwned API Key', placeholder: 'your-hibp-key',         primary: false },
  { key: 'IPINFO_TOKEN',        label: 'IPInfo Token',           placeholder: 'your-ipinfo-token',     primary: false },
  { key: 'IP2LOCATION_API_KEY', label: 'IP2Location API Key',    placeholder: 'your-ip2location-key',  primary: false },
  { key: 'CENSYS_API_ID',       label: 'Censys API ID',          placeholder: 'censys-api-id',         primary: false },
  { key: 'CENSYS_SECRET',       label: 'Censys API Secret',      placeholder: 'censys-api-secret',     primary: false },
  { key: 'SHODAN_API_KEY',      label: 'Shodan API Key',         placeholder: 'your-shodan-key',       primary: false },
  { key: 'VIRUSTOTAL_API_KEY',  label: 'VirusTotal API Key',     placeholder: 'your-virustotal-key',   primary: false },
]