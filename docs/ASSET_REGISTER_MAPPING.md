# Asset Register Mapping

## Workflow

`Source Asset Register -> external mapping/transformation -> canonical import -> validation -> simulator`

The simulator should not guess ambiguous source columns in production.

## Minimal canonical profile

Required core fields are `caisse_id`, `site_id`, `site_name`, `asset_type`, `asset_status`, `city`, `province_code`, `country_code`, `gross_floor_area`, `area_unit`, `tenure_type`, `source_system`, and `source_record_id`.

Recommended fields include Caisse/site names, address, postal code, latitude/longitude, year built, lease expiry, region and source as-of date.

## OSCRE alignment

This profile is intentionally **OSCRE-aligned**, not declared OSCRE-conformant. OSCRE IDM is use-case based; exact entity/attribute identifiers must be mapped against the authoritative OSCRE schema/rendition selected by the organization.

Maintain a mapping dictionary with:

- source attribute
- canonical attribute
- transformation
- required flag
- OSCRE concept/entity
- OSCRE attribute
- OSCRE use case
- OSCRE definition
- internal extension yes/no

## Keep linked analytical products separate

Technical/Functional/Capacity backlog, CRV assumptions, energy, carbon, service demand/capacity and strategic scores are not automatically Asset Register identity fields. Link them through stable identifiers and retain provenance.
