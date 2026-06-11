# Legacy Carmen Notes

The original `GenBill/Carmen` repository is a legacy reference only.

CarmenV must not copy legacy code or migrate the old mixed structure. The new system starts from a clean attribution-first architecture with stable schemas, deterministic candidate generation, structured scores, persisted intermediate results, and forward-return labels.

Future migration can treat old Carmen daily output as another candidate source, for example `source="legacy_carmen"`. In that mode, the legacy system remains a baseline input for attribution rather than the architectural foundation of CarmenV.
