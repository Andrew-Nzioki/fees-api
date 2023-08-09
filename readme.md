flask db init
flask db migrate -m "Initial migration."
flask db upgrade

# PAYLOAD

1. JSON payload for `User` model:

```json
{
  "name": "John Doe",
  "group": "Group A",
  "is_client": true,
  "is_admin": false
}
```

2. JSON payload for `Fees` model:

```json
{
  "record": 123,
  "file_reference": "ABC123",
  "clients_reference": "ClientRef123",
  "case_no_or_parties": "Case123",
  "deposit_fees": 1000,
  "final_fees": 2000,
  "deposit_pay": 500,
  "final_pay": 1500,
  "outstanding": 1000,
  "deposit": 200,
  "user_id": 1
}
```

3. JSON payload for `Document` model:

```json
{
  "name": "DocumentName123",
  "user_id": 1
}
```

4. JSON payload for `Case` model:

```json
{
  "description": "CaseDescription123",
  "user_id": 1
}
```
