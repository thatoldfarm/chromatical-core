# LOADING IRONVAULT_LOADER (index.html) locally:

---

# Launch a local python HTTP server:

```python
python3 -m http.server 8000
```

---

- **OR:**

# Launch a local web browser in an 'insecure' manner.


```bash
chromium %U --user-data-dir="~/chrome-dev-disabled-security" --disable-web-security --disable-site-isolation-trials --allow-file-access-from-files --allow-insecure-localhost ./index.html
```
