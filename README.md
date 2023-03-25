# fb-zoo
`Run:` python3 -m app.main

order of method calls: 
- app/main.py
- app/bot_run.py
    - database/bot_sql.py
    - tools/vpn_selector.py
    - browser/browser_properties.py
    - core/coordination/core.py
- core/coordination/core.py
    - core/coordination/model.py
    - actions/random_range.py
    - actions/cookies.py
    - core/features/login.py
- core/coordination/model.py
    core/features*