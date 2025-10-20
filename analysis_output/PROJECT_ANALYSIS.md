# Projekt-Analyse: 

**Analyse-Datum:** 2025-10-20T10:12:04.277304

## 📊 Übersicht

- **Dateien:** 363
- **Zeilen Code:** 37,186
- **Dependencies:** 37
- **Frameworks:** 25

## 🌐 Programmiersprachen

- Python
- Markdown
- XML
- JSON
- YAML
- JavaScript
- Shell
- HTML
- Mobile App
- Python Docker

## 🛠️ Frameworks & Libraries

- **React** (Frontend)
- **Docker** (Library)
- **Node.js** (Library)
- **pytest** (Testing)
- **Python** (Library)
- **FastAPI** (Backend)
- **Celery** (Library)
- **Vue** (Frontend)
- **Angular** (Frontend)
- **Express.js** (Frontend)
- **unittest** (Testing)
- **Flask** (Backend)
- **Next.js** (Frontend)
- **SQLAlchemy** (Database)
- **Django** (Backend)
- **Jest** (Testing)
- **Bootstrap** (CSS Framework)
- **Sass** (CSS Framework)
- **Pyramid** (Backend)
- **Nuxt.js** (Frontend)
- **React Native** (Mobile)
- **Mongoose** (Database)
- **Mocha** (Testing)
- **Prisma** (Database)
- **Tailwind CSS** (CSS Framework)

## 🔒 Security-Issues

- **HIGH:** FastAPI 0.109.1 addresses a critical security issue by upgrading its dependency python-multipart to version >=0.0.7. The upgrade mitigates a Regular Expression Denial of Service (ReDoS) vulnerability, which occurs when parsing form data. 
https://github.com/tiangolo/fastapi/security/advisories/GHSA-qf9m-vfgh-m389
- **HIGH:** Fastapi 0.109.1 updates its minimum version of 'python-multipart' to >=0.0.7 to include a security fix.
- **HIGH:** Affected versions of python-multipart are vulnerable to Allocation of Resources Without Limits or Throttling (CWE-770). An attacker can send specially crafted multipart/form-data requests containing excessive CR (\r) or LF (\n) characters before the first boundary or after the last boundary. This can lead to uncontrolled CPU usage and high memory consumption, causing the processing thread or event loop in ASGI applications to stall, resulting in a denial of service (DoS). The vulnerability exists in the MultipartParser's handling of line breaks around boundaries, where it processes each CRLF byte individually and logs warnings for each occurrence. To exploit this, an attacker simply needs to send large amounts of malformed multipart data with numerous CRLF characters. Upgrading to version 0.0.19 resolves this issue by preventing excessive resource allocation and logging when CRLF bytes are present.
- **HIGH:** A vulnerability in versions of python-multipart before 0.0.7 involves a Regular Expression Denial of Service (ReDoS) triggered by custom Content-Type headers. This issue allows an attacker to cause a significant consumption of system resources while processing such headers, effectively preventing the processing of other requests. This ReDoS vulnerability stems from the way regular expressions evaluate certain input patterns, which can lead to extensive backtracking, thereby causing the application to slow down significantly, consuming a disproportionate amount of CPU time and facilitating a denial of service condition.
- **HIGH:** A vulnerability in the Jinja compiler allows an attacker who can control both the content and filename of a template to execute arbitrary Python code, bypassing Jinja's sandbox protections. To exploit this vulnerability, an attacker must have the ability to manipulate both the template's filename and its contents. The risk depends on the application's specific use case. This issue affects applications that render untrusted templates where the attacker can determine the template filename, potentially leading to severe security breaches.
- **HIGH:** An oversight in how the Jinja sandboxed environment detects calls to str.format allows an attacker who controls the content of a template to execute arbitrary Python code. To exploit the vulnerability, an attacker needs to control the content of a template. Whether that is the case depends on the type of application using Jinja. This vulnerability impacts users of applications which execute untrusted templates. Jinja's sandbox does catch calls to str.format and ensures they don't escape the sandbox. However, it's possible to store a reference to a malicious string's format method, then pass that to a filter that calls it. No such filters are built-in to Jinja, but could be present through custom filters in an application. After the fix, such indirect calls are also handled by the sandbox.
- **HIGH:** Jinja is an extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. It is possible to inject arbitrary HTML attributes into the rendered HTML template, potentially leading to Cross-Site Scripting (XSS). The Jinja `xmlattr` filter can be abused to inject arbitrary HTML attribute keys and values, bypassing the auto escaping mechanism and potentially leading to XSS. It may also be possible to bypass attribute validation checks if they are blacklist-based.
- **HIGH:** Jinja is an extensible templating engine. The `xmlattr` filter in affected versions of Jinja accepts keys containing non-attribute characters. XML/HTML attributes cannot contain spaces, `/`, `>`, or `=`, as each would then be interpreted as starting a separate attribute. If an application accepts keys (as opposed to only values) as user input, and renders these in pages that other users see as well, an attacker could use this to inject other attributes and perform XSS. The fix for CVE-2024-22195 only addressed spaces but not other characters. Accepting keys as user input is now explicitly considered an unintended use case of the `xmlattr` filter, and code that does so without otherwise validating the input should be flagged as insecure, regardless of Jinja version. Accepting _values_ as user input continues to be safe.
- **HIGH:** Prior to 3.1.6, an oversight in how the Jinja sandboxed environment interacts with the |attr filter allows an attacker that controls the content of a template to execute arbitrary Python code. To exploit the vulnerability, an attacker needs to control the content of a template. Whether that is the case depends on the type of application using Jinja. This vulnerability impacts users of applications which execute untrusted templates. Jinja's sandbox does catch calls to str.format and ensures they don't escape the sandbox. However, it's possible to use the |attr filter to get a reference to a string's plain format method, bypassing the sandbox. After the fix, the |attr filter no longer bypasses the environment's attribute lookup. This vulnerability is fixed in 3.1.6.
- **HIGH:** In Streamlit affected versions, users hosting Streamlit app(s) that use custom components are vulnerable to a directory traversal attack that could leak data from their web server file-system such as: server logs, world-readable files, and potentially other sensitive information. An attacker can craft a malicious URL with file paths and the streamlit server would process that URL and return the contents of that file. This issue has been resolved in version 1.11.1. Users are advised to upgrade. There are no known workarounds for this issue.
- **HIGH:** Affected versions of the `Streamlit` package are vulnerable to Path Traversal due to improper handling of file paths in the static file sharing feature. The static file sharing feature fails to sanitize user input, allowing crafted file paths to access arbitrary files on the server. An attacker can exploit this vulnerability on Windows systems to leak sensitive information, such as the password hash of the Windows user running `Streamlit`, by accessing unauthorized files.
- **HIGH:** Versions of the package pymongo before 4.6.3 are vulnerable to Out-of-bounds Read in the bson module. Using the crafted payload the attacker could force the parser to deserialize unmanaged memory. The parser tries to interpret bytes next to buffer and throws an exception with string. If the following bytes are not printable UTF-8 the parser throws an exception with a single byte.
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded database_url gefunden
- **HIGH:** Potentieller hardcoded password gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded database_url gefunden
- **HIGH:** Potentieller hardcoded password gefunden
- **HIGH:** Potentieller hardcoded password gefunden
- **HIGH:** Potentieller hardcoded password gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded password gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded token gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded api_key gefunden
- **HIGH:** Potentieller hardcoded database_url gefunden
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: shell
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: shell
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: crypto_weak
- **HIGH:** Potentielles Security-Risiko: eval
- **HIGH:** Potentielles Security-Risiko: eval
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **MEDIUM:** Potentielles Security-Risiko: subprocess
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: xss
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: xss
- **HIGH:** Potentielles Security-Risiko: eval
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: xss
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: xss
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: xss
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: xss
- **MEDIUM:** Potentielles Security-Risiko: xss
- **HIGH:** Potentielles Security-Risiko: exec
- **MEDIUM:** Potentielles Security-Risiko: xss

## 🧪 Test-Coverage

- **Coverage:** 6.5%
- **Test-Frameworks:** unittest, pytest
- **Test-Dateien:** 8

