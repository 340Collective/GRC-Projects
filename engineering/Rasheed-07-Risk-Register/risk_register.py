"""Offline Project 07 prototype. Use only synthetic register data."""

import argparse
from collections import defaultdict
from datetime import date, timedelta
from html import escape
import json
from pathlib import Path
import re


CATEGORIES = {"Security", "Vendor", "Business"}
FIELDS = {
    "risk_id", "category", "description", "owner_role", "mitigation",
    "likelihood", "impact", "residual_likelihood", "residual_impact", "assessed_on",
}


def score(likelihood, impact):
    if any(type(value) is not int or not 1 <= value <= 5 for value in (likelihood, impact)):
        raise ValueError("Likelihood and impact must be integers from 1 to 5.")
    value = likelihood * impact
    if value >= 15:
        rating, color, days = "High", "red", 30
    elif value >= 7:
        rating, color, days = "Medium", "amber", 90
    else:
        rating, color, days = "Low", "green", 180
    return {"value": value, "rating": rating, "color": color, "review_days": days}


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise ValueError("Dates must use YYYY-MM-DD.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError("Dates must be valid calendar dates.") from None


def assess_risk(item, as_of):
    if not isinstance(item, dict) or set(item) != FIELDS:
        raise ValueError("Each risk must contain exactly the documented input fields.")
    risk_id = item["risk_id"]
    if not isinstance(risk_id, str) or not re.fullmatch(r"R-(?!000)[0-9]{3}", risk_id):
        raise ValueError("Risk IDs must use R-001 through R-999.")
    category = item["category"]
    if not isinstance(category, str) or category not in CATEGORIES:
        raise ValueError("Category must be Security, Vendor or Business.")
    clean = dict(item)
    for field in ("description", "owner_role", "mitigation"):
        value = item[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be non-empty text.")
        clean[field] = value.strip()
    if clean["mitigation"].rstrip(".!? ").casefold() == "monitor":
        raise ValueError("Mitigation must name a specific action.")

    inherent = score(item["likelihood"], item["impact"])
    residual = score(item["residual_likelihood"], item["residual_impact"])
    if residual["value"] > inherent["value"]:
        raise ValueError("Residual score cannot exceed inherent score.")
    assessed_on = parse_date(item["assessed_on"])
    if assessed_on > as_of:
        raise ValueError("Assessment date cannot be after the report date.")
    try:
        review_date = assessed_on + timedelta(days=inherent["review_days"])
    except OverflowError:
        raise ValueError("Review date is outside the supported calendar range.") from None
    return {
        **clean,
        "inherent": inherent,
        "residual": residual,
        "review_date": review_date.isoformat(),
        "review_due": as_of >= review_date,
        "requires_issm_acceptance": residual["rating"] == "High",
    }


def assess_register(items, as_of):
    if not isinstance(items, list):
        raise ValueError("Register input must be a JSON array of risks.")
    if type(as_of) is not date:
        raise ValueError("Report date must be a date without a time.")
    risks = []
    seen = set()
    positions = defaultdict(list)
    for index, item in enumerate(items, 1):
        try:
            risk = assess_risk(item, as_of)
        except ValueError as error:
            raise ValueError(f"Risk row {index}: {error}") from None
        risk_id = risk["risk_id"]
        if risk_id in seen:
            raise ValueError(f"Risk row {index}: duplicate risk ID.")
        seen.add(risk_id)
        positions[risk["likelihood"], risk["impact"]].append(risk_id)
        risks.append(risk)
    risks.sort(key=lambda risk: risk["risk_id"])
    heatmap = [
        {"likelihood": likelihood, "impact": impact, "rating": score(likelihood, impact)["rating"],
         "risk_ids": sorted(positions[likelihood, impact])}
        for likelihood in range(5, 0, -1) for impact in range(1, 6)
    ]
    return {
        "mode": "offline_simulation",
        "scoring_model": "likelihood_x_impact",
        "as_of": as_of.isoformat(),
        "risks": risks,
        "heatmap": heatmap,
        "top_five": sorted(risks, key=lambda risk: (-risk["inherent"]["value"], risk["risk_id"]))[:5],
        "review_due_ids": [risk["risk_id"] for risk in risks if risk["review_due"]],
        "acceptance_required_ids": [risk["risk_id"] for risk in risks if risk["requires_issm_acceptance"]],
    }


def render_html(report):
    def safe(value):
        return escape(str(value), quote=True)

    rows = []
    for start in range(0, 25, 5):
        cells = report["heatmap"][start:start + 5]
        row = f'<tr><th scope="row">{safe(cells[0]["likelihood"])}</th>'
        for cell in cells:
            rating = safe(cell["rating"])
            ids = safe(", ".join(cell["risk_ids"]) or "None")
            row += f'<td class="{rating.lower()}">{rating}<br>{ids}</td>'
        rows.append(row + "</tr>")
    leaders = []
    for risk in report["top_five"]:
        fields = (risk["risk_id"], risk["description"], risk["owner_role"],
                  risk["inherent"]["value"], risk["residual"]["value"], risk["review_date"])
        leaders.append("<tr>" + "".join(f"<td>{safe(value)}</td>" for value in fields) + "</tr>")
    return f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><title>Risk Register simulation</title>
<style>
body {{font: 16px system-ui; color: #192b3d; margin: 2rem;}}
table {{border-collapse: collapse; margin-bottom: 1.5rem;}}
th, td {{border: 1px solid #586879; padding: .5rem; text-align: left;}}
.high {{background: #ffd6d6;}} .medium {{background: #ffe8af;}} .low {{background: #d6f0dc;}}
</style>
<h1>Risk Register simulation</h1>
<p>Synthetic inputs. As of {safe(report['as_of'])}. Score: likelihood multiplied by impact.</p>
<p>Reviews due: {safe(', '.join(report['review_due_ids']) or 'None')}.</p>
<p>Written ISSM acceptance required: {safe(', '.join(report['acceptance_required_ids']) or 'None')}.</p>
<table><caption>Inherent risk heat map: rows are likelihood, columns are impact</caption>
<thead><tr><th scope="col">Likelihood / Impact</th><th scope="col">1</th><th scope="col">2</th>
<th scope="col">3</th><th scope="col">4</th><th scope="col">5</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<table><caption>Top five by inherent score</caption><thead><tr><th scope="col">Risk ID</th>
<th scope="col">Description</th><th scope="col">Owner role</th><th scope="col">Score</th>
<th scope="col">Residual</th><th scope="col">Review date</th></tr></thead>
<tbody>{''.join(leaders)}</tbody></table></html>"""


def unique_fields(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Duplicate JSON fields are not allowed.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Synthetic risk records in a JSON file")
    parser.add_argument("--as-of", required=True, help="Report date (YYYY-MM-DD)")
    parser.add_argument("--format", choices=("json", "html"), default="json")
    args = parser.parse_args()
    try:
        path = args.input.resolve()
        if path.suffix.lower() != ".json" or not path.is_file() or "private-evidence" in path.parts:
            raise ValueError("Use an existing synthetic JSON file outside private evidence.")
        with path.open(encoding="utf-8") as handle:
            items = json.load(handle, object_pairs_hook=unique_fields)
        report = assess_register(items, parse_date(args.as_of))
    except (OSError, UnicodeError):
        parser.error("Unable to read the synthetic JSON input.")
    except ValueError as error:
        parser.error(str(error))
    print(render_html(report) if args.format == "html" else json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
