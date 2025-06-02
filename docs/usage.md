# API Usage

## `/next_bonus`

### Method: `POST`
Returns the €/km uplift matrix for the next 15 minutes.

**Request:**
```json
{
  "timestamp": "2024-06-01T14:00:00Z",
  "area_ids": ["area_123", "area_456"]
}
```

**Response:**
```json
{
  "status": "ok",
  "matrix": {
    "area_123": 0.15,
    "area_456": 0.25
  },
  "explanation": "High lunch demand in downtown. ADWIN and forecast agree on uplift."
}
```

## `/health`

Simple health check endpoint.

## Slack Bot

When a bonus uplift is published, a Slack message is posted to the configured webhook:

```
📈 Bonus updated: Downtown +0.25 €/km for next 15 minutes.
📊 Reason: Spike detected via ADWIN + forecast confirms demand.
```