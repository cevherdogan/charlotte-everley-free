# Working Cursor

## Branch
refactor/bronze-premier-migration

## Last Completed
- Gallery: data-tier fixed, JS uses `.card`, Bronze/Premier styles added
- access_map.json: plans = [bronze, free, premier, silver]
- Filenames normalized (_trial → _bronze, -gold → -premier)

## Next Actions
- Run `scripts/check_tiers.sh` (should pass)
- Run CLI simulate: `scripts/simulate_rbac_access.py`
- Serve gallery and click through links
- Decide fate of rbac-map.json (keep synced or retire)
- If green → merge into dev/rbac-tiered-access

## Open Questions
- Keep membership/gold & membership/trial as historical? Or redirect?
