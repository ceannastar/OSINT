import asyncio


# Каталог инструментов (только для схемы)
TOOL_CATALOG: list[dict] = [
    {
        "name": "search_email",
        "description": "Enumerate accounts linked to an email via holehe.",
        "input_label": "Email address",
        "input_placeholder": "target@example.com",
    },
    {
        "name": "search_username",
        "description": "Enumerate platforms where a username is registered.",
        "input_label": "Username",
        "input_placeholder": "johndoe99",
    },
    {
        "name": "search_ip",
        "description": "Retrieve geolocation and ASN data for an IP address.",
        "input_label": "IP address",
        "input_placeholder": "8.8.8.8",
    },
    {
        "name": "search_domain",
        "description": "Enumerate subdomains of a target domain.",
        "input_label": "Domain",
        "input_placeholder": "example.com",
    },
]

OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": f"{tool['input_label']} — e.g. {tool['input_placeholder']}",
                    }
                },
                "required": ["input"],
            },
        },
    }
    for tool in TOOL_CATALOG
]


async def run_tool(tool_name: str, tool_input: str) -> str:
    await asyncio.sleep(1.5)
    
    if tool_name == "search_email":
        return (
            "[+] Spotify       https://open.spotify.com/user/demo\n"
            "[+] GitHub        https://github.com/demo\n"
            "[+] Gravatar      https://gravatar.com/demo\n"
            "[*] Holehe scan complete — 3 accounts found"
        )
    elif tool_name == "search_username":
        return (
            "[+] Twitter       https://twitter.com/demo\n"
            "[+] GitHub        https://github.com/demo\n"
            "[+] Reddit        https://reddit.com/user/demo\n"
            "[*] Sherlock scan complete — 3 platforms found"
        )
    elif tool_name == "search_ip":
        return (
            "[+] IP: 8.8.8.8\n"
            "[+] Hostname: dns.google\n"
            "[+] Country: US — Mountain View, California\n"
            "[+] Org: AS15169 Google LLC"
        )
    elif tool_name == "search_domain":
        return (
            "[+] Subdomains found:\n"
            "  - www.example.com\n"
            "  - mail.example.com\n"
            "  - api.example.com\n"
            "[*] Sublist3r scan complete — 3 subdomains found"
        )
    else:
        return f"[*] Неизвестный инструмент: {tool_name}"